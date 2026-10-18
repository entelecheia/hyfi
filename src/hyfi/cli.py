"""``hyfi`` command line. Trailing arguments are Hydra overrides; ``--json`` output is for agents.

Exit codes: 0 success, 1 the run or check failed, 2 usage or config error.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, NoReturn

from omegaconf import OmegaConf
from pydantic import BaseModel

from hyfi import plugins as _plugins
from hyfi._version import __version__
from hyfi.config import compose, to_dict
from hyfi.manifest import RunManifest
from hyfi.project import Project
from hyfi.runner import load_workflow, record_config, run_workflow
from hyfi.workflow import Workflow, plan

logger = logging.getLogger("hyfi")


class UsageError(Exception):
    pass


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise UsageError(f"{self.prog}: {message}")


SCHEMAS: dict[str, type[BaseModel]] = {"project": Project, "workflow": Workflow}
ALLOW_HELP = "allowed step target, exact or pkg.* (repeatable; also $HYFI_ALLOW, comma-separated)"


def _emit(data: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    elif isinstance(data, str):
        print(data)
    else:
        print(OmegaConf.to_yaml(OmegaConf.create(data)), end="")


def _compose_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("overrides", nargs="*", help="Hydra overrides, e.g. workflow=demo a.b=1")
    p.add_argument("--config-dir", help="user config directory (default: ./conf if present)")
    p.add_argument("--config-name", default="config", help="primary config name")
    p.add_argument("--json", action="store_true", help="machine-readable output")


def _compose(ns: argparse.Namespace) -> Any:
    return compose(ns.overrides, config_name=ns.config_name, config_dir=ns.config_dir)


def cmd_config_show(ns: argparse.Namespace) -> int:
    _emit(to_dict(_compose(ns), resolve=not ns.no_resolve), ns.json)
    return 0


def cmd_config_schema(ns: argparse.Namespace) -> int:
    target = ns.target
    if target in SCHEMAS:
        model = SCHEMAS[target]
    else:
        from hydra.utils import get_class

        model = get_class(target)
        if not (isinstance(model, type) and issubclass(model, BaseModel)):
            raise TypeError(f"{target} is not a Pydantic model")
    print(json.dumps(model.model_json_schema(), indent=2, ensure_ascii=False))
    return 0


def cmd_plugins(ns: argparse.Namespace) -> int:
    rows = [
        {
            "name": p.name,
            "module": p.module,
            "distribution": p.distribution,
            "available": p.available,
        }
        for p in _plugins.discover()
    ]
    if ns.json:
        _emit(rows, True)
    else:
        for r in rows:
            mark = "ok" if r["available"] else "MISSING"
            print(f"{r['name']}\t{r['module']}\t{r['distribution'] or '-'}\t{mark}")
    return 0


def _allow(ns: argparse.Namespace, recorded: list[str] | None = None) -> list[str] | None:
    """``--allow`` flags plus ``HYFI_ALLOW``; None (no checks) when neither is given."""
    env = [p.strip() for p in os.environ.get("HYFI_ALLOW", "").split(",") if p.strip()]
    given = [*(ns.allow or []), *env]
    return given or recorded


def _dry_run(config: Any, as_json: bool, allow: list[str] | None) -> int:
    resolved, recorded = record_config(config)
    _, workflow = load_workflow(resolved)
    _, shown = load_workflow(recorded)
    steps = plan(workflow, allow=allow)
    for entry, step in zip(steps, shown.steps, strict=True):  # print the recorded view only
        entry["run"], entry["with"] = step.run, step.with_
    _emit({"workflow": workflow.name, "steps": steps}, as_json)
    return 0 if all(s["ok"] for s in steps) else 1


def _report(manifest: RunManifest, as_json: bool) -> int:
    if as_json:
        _emit(manifest.model_dump(mode="json"), True)
    else:
        print(f"run {manifest.run_id}: {manifest.status}")
        for s in manifest.steps:
            took = f" ({s.seconds}s)" if s.seconds is not None else ""
            print(f"  {s.status:8} {s.name}{took}{'  ' + s.error if s.error else ''}")
        runs_dir = Project.model_validate(manifest.config.get("project") or {}).runs_dir
        print(f"manifest: {runs_dir / manifest.run_id / 'manifest.json'}")
    return 0 if manifest.status == "ok" else 1


def cmd_run(ns: argparse.Namespace) -> int:
    cfg = _compose(ns)
    allow = _allow(ns)
    if ns.dry_run:
        return _dry_run(cfg, ns.json, allow)
    manifest = run_workflow(
        cfg,
        overrides=ns.overrides,
        config_name=ns.config_name,
        config_dir=ns.config_dir,
        argv=ns.argv,
        allow=allow,
    )
    return _report(manifest, ns.json)


def cmd_rerun(ns: argparse.Namespace) -> int:
    root = Path(ns.root or os.environ.get("HYFI_PROJECT_ROOT") or ".")
    runs_dir = Project(root=root).runs_dir
    original = RunManifest.load(ns.run_id, runs_dir)
    allow = _allow(ns, recorded=original.allow)
    if ns.dry_run:
        return _dry_run(original.config, ns.json, allow)
    manifest = run_workflow(
        original.config,
        overrides=original.overrides,
        config_name=original.config_name,
        config_dir=original.config_dir,
        argv=ns.argv,
        rerun_of=original.run_id,
        allow=allow,
    )
    return _report(manifest, ns.json)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="hyfi", description=__doc__.splitlines()[0])
    parser.add_argument("--version", action="version", version=f"hyfi {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    config = sub.add_parser("config", help="inspect configs").add_subparsers(
        dest="config_command", required=True
    )
    show = config.add_parser("show", help="print the composed config")
    _compose_args(show)
    show.add_argument("--no-resolve", action="store_true", help="keep ${...} interpolations")
    show.set_defaults(func=cmd_config_show)
    schema = config.add_parser("schema", help="print a JSON Schema")
    schema.add_argument(
        "target",
        nargs="?",
        default="workflow",
        help="project, workflow, or a dotted Pydantic model",
    )
    schema.add_argument(
        "--json", action="store_true", help="accepted for uniformity; output is JSON"
    )
    schema.set_defaults(func=cmd_config_schema)

    plugins = sub.add_parser("plugins", help="list installed plugins")
    plugins.add_argument("--json", action="store_true")
    plugins.set_defaults(func=cmd_plugins)

    run = sub.add_parser("run", help="run the selected workflow and write a manifest")
    _compose_args(run)
    run.add_argument("--dry-run", action="store_true", help="resolve steps without running them")
    run.add_argument("--allow", action="append", metavar="PATTERN", help=ALLOW_HELP)
    run.set_defaults(func=cmd_run)

    rerun = sub.add_parser("rerun", help="run a recorded config again")
    rerun.add_argument("run_id")
    rerun.add_argument(
        "--root",
        help="where to find .hyfi/runs (default: $HYFI_PROJECT_ROOT or .); "
        "the rerun writes to the recorded project root",
    )
    rerun.add_argument("--dry-run", action="store_true")
    rerun.add_argument(
        "--allow", action="append", metavar="PATTERN", help=ALLOW_HELP + "; default: as recorded"
    )
    rerun.add_argument("--json", action="store_true")
    rerun.set_defaults(func=cmd_rerun)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=os.environ.get("HYFI_LOG_LEVEL", "WARNING"), stream=sys.stderr)
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        ns = build_parser().parse_args(args)
    except UsageError as e:
        if "--json" in args:
            print(json.dumps({"error": f"UsageError: {e}"}))
        print(f"{e}\nRun 'hyfi --help' for usage.", file=sys.stderr)
        return 2
    ns.argv = ["hyfi", *args]
    try:
        code: int = ns.func(ns)
    except Exception as e:  # report every failure the same way, then exit non-zero
        if getattr(ns, "json", False):
            print(json.dumps({"error": f"{type(e).__name__}: {e}"}), file=sys.stdout)
        print(f"hyfi: error: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    return code


if __name__ == "__main__":
    raise SystemExit(main())

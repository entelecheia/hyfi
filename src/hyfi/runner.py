"""Run the ``workflow`` node of a composed config and record a manifest."""

from __future__ import annotations

import os
import re
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from omegaconf import DictConfig, OmegaConf

from hyfi.config import to_dict
from hyfi.manifest import RunManifest, git_info, lock_sha256
from hyfi.project import Project
from hyfi.workflow import Workflow, WorkflowError, execute

ENV_REF = re.compile(r"oc\.env:\s*([A-Za-z_][A-Za-z0-9_]*)")
MIN_REDACT_LEN = 4  # shorter values (flags, "1", ".") would mangle unrelated text


def env_replacements(raw: Any) -> dict[str, str]:
    """Map the current value of every env var named in an ``oc.env:`` reference to its interpolation."""
    names: set[str] = set()
    stack = [raw]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            stack.extend(node.values())
        elif isinstance(node, list | tuple):
            stack.extend(node)
        elif isinstance(node, str):
            names.update(ENV_REF.findall(node))
    found: dict[str, str] = {}
    for name in sorted(names):
        value = os.environ.get(name, "")
        if len(value) >= MIN_REDACT_LEN:
            found.setdefault(value, "${oc.env:" + name + "}")
    return found


def redact(obj: Any, replacements: dict[str, str]) -> Any:
    """Replace every occurrence of a secret value in every string (keys included) of ``obj``."""
    if not replacements:
        return obj
    ordered = sorted(replacements, key=len, reverse=True)

    def fix(text: str) -> str:
        for value in ordered:
            text = text.replace(value, replacements[value])
        return text

    def walk(node: Any) -> Any:
        if isinstance(node, str):
            return fix(node)
        if isinstance(node, dict):
            return {walk(k): walk(v) for k, v in node.items()}
        if isinstance(node, list | tuple):
            return [walk(v) for v in node]
        return node

    return walk(obj)


def keep_env_interpolations(resolved: Any, raw: Any) -> Any:
    """``resolved``, except leaves whose unresolved form reads ``${oc.env:...}`` stay unresolved.

    Values from the environment (often secrets) are re-read on rerun instead of being recorded.
    """
    if isinstance(resolved, dict) and isinstance(raw, dict):
        return {k: keep_env_interpolations(v, raw.get(k)) for k, v in resolved.items()}
    if isinstance(resolved, list) and isinstance(raw, list) and len(resolved) == len(raw):
        return [keep_env_interpolations(a, b) for a, b in zip(resolved, raw, strict=True)]
    if isinstance(raw, str) and "oc.env:" in raw:
        return raw
    return resolved


def record_config(config: Any) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    """Return ``(resolved, recorded, replacements)`` for a composed or recorded config.

    ``resolved`` is what runs. ``recorded`` is the config view written to manifests and printed:
    ``${oc.env:...}`` leaves stay unresolved, ``project.root`` / ``project.workspace`` become
    absolute paths, and every env value from ``replacements`` is replaced by its interpolation.
    Callers apply :func:`redact` with ``replacements`` to anything else they emit (names, errors).
    """
    # ponytail: a recorded literal "${...}" (escaped in the original) is re-read as interpolation.
    cfg = config if isinstance(config, DictConfig) else OmegaConf.create(to_dict(config))
    resolved: dict[str, Any] = to_dict(cfg)
    recorded: dict[str, Any] = keep_env_interpolations(resolved, to_dict(cfg, resolve=False))
    if "project" in resolved:
        project = Project.model_validate(resolved.get("project") or {})
        recorded["project"] = {
            **(recorded.get("project") or {}),
            "root": str(project.root),
            "workspace": str(project.workspace),
        }
    replacements = env_replacements(to_dict(cfg, resolve=False))
    return resolved, redact(recorded, replacements), replacements


def load_workflow(config: Any) -> tuple[Project, Workflow]:
    """Validate the ``project`` and ``workflow`` nodes of a composed (or recorded) config."""
    data = to_dict(config)
    if not data.get("workflow"):
        raise ValueError("no workflow selected: pass an override such as workflow=<name>")
    project = Project.model_validate(data.get("project") or {})
    return project, Workflow.model_validate(data["workflow"])


def run_workflow(
    config: Any,
    *,
    overrides: Sequence[str] = (),
    config_name: str | None = None,
    config_dir: str | None = None,
    argv: Sequence[str] = (),
    rerun_of: str | None = None,
    allow: Sequence[str] | None = None,
) -> RunManifest:
    """Execute the workflow and write ``<project.root>/.hyfi/runs/<run_id>/manifest.json``.

    The manifest is written before the first step and again at the end, so a crash leaves a
    ``running`` record. Step failures are recorded, not raised; check ``manifest.status``.
    ``allow`` is the execution allowlist (see :func:`hyfi.config.instantiate`).
    """
    resolved, recorded, replacements = record_config(config)
    project, workflow = load_workflow(resolved)
    manifest = RunManifest(
        rerun_of=rerun_of,
        argv=list(argv),
        config_name=config_name,
        config_dir=config_dir,
        overrides=list(overrides),
        allow=list(allow) if allow is not None else None,
        config=recorded,
        git=git_info(project.root),
        lock_sha256=lock_sha256(project.root),
    )
    runs_dir = project.runs_dir

    def redacted() -> RunManifest:  # step names and errors can carry env values too
        return RunManifest.model_validate(redact(manifest.model_dump(mode="json"), replacements))

    redacted().write(runs_dir)
    try:
        _, manifest.steps = execute(workflow, allow=allow)
        manifest.status = "ok"
    except WorkflowError as e:
        manifest.steps, manifest.status, manifest.error = e.records, "error", str(e)
    finally:
        manifest.finished_at = datetime.now(UTC)
        result = redacted()
        result.write(runs_dir)
    return result

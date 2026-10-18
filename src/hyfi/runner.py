"""Run the ``workflow`` node of a composed config and record a manifest."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from omegaconf import DictConfig, OmegaConf

from hyfi.config import to_dict
from hyfi.manifest import RunManifest, git_info, lock_sha256
from hyfi.project import Project
from hyfi.workflow import Workflow, WorkflowError, execute


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


def record_config(config: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(resolved, recorded)`` views of a composed or recorded config.

    ``resolved`` is what runs. ``recorded`` is the only view written to manifests, ``--json`` run
    output, and dry-run plans: ``${oc.env:...}`` leaves stay unresolved, and ``project.root`` /
    ``project.workspace`` become absolute paths so a rerun writes to the original project.
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
    return resolved, recorded


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
    resolved, recorded = record_config(config)
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
    manifest.write(runs_dir)
    try:
        _, manifest.steps = execute(workflow, allow=allow)
        manifest.status = "ok"
    except WorkflowError as e:
        manifest.steps, manifest.status, manifest.error = e.records, "error", str(e)
    finally:
        manifest.finished_at = datetime.now(UTC)
        manifest.write(runs_dir)
    return manifest

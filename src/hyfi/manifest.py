"""Run manifests: what ran, with which resolved config, on which code, and how it went."""

from __future__ import annotations

import hashlib
import json
import platform
import secrets
import subprocess  # nosec B404: fixed git argv only
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from hyfi._version import __version__
from hyfi.workflow import StepRecord

MANIFEST_NAME = "manifest.json"


def new_run_id() -> str:
    return f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{secrets.token_hex(3)}"


def git_info(cwd: Path) -> dict[str, Any] | None:
    """HEAD SHA and dirty flag of the repository containing ``cwd``; None outside a repository."""

    def git(*args: str) -> str:
        return subprocess.run(  # noqa: S603
            ["git", *args],  # noqa: S607
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        ).stdout.strip()

    try:
        return {"sha": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain"))}
    except (OSError, subprocess.SubprocessError):
        return None


def lock_sha256(root: Path) -> str | None:
    lock = root / "uv.lock"
    return hashlib.sha256(lock.read_bytes()).hexdigest() if lock.is_file() else None


class RunManifest(BaseModel):
    run_id: str = Field(default_factory=new_run_id)
    rerun_of: str | None = None
    status: Literal["running", "ok", "error"] = "running"
    error: str | None = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None
    hyfi_version: str = __version__
    python: str = Field(default_factory=lambda: sys.version.split()[0])
    platform: str = Field(default_factory=platform.platform)
    argv: list[str] = Field(default_factory=list)
    config_name: str | None = None
    config_dir: str | None = None
    overrides: list[str] = Field(default_factory=list)
    allow: list[str] | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    git: dict[str, Any] | None = None
    lock_sha256: str | None = None
    steps: list[StepRecord] = Field(default_factory=list)

    def config_json(self) -> str:
        """Canonical JSON of the resolved config, for byte-level comparison."""
        return json.dumps(self.config, sort_keys=True, ensure_ascii=False)

    def write(self, runs_dir: Path) -> Path:
        path = runs_dir / self.run_id / MANIFEST_NAME
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(self.model_dump_json(indent=2), encoding="utf-8")
        tmp.replace(path)
        return path

    @classmethod
    def load(cls, run_id: str, runs_dir: Path) -> RunManifest:
        path = runs_dir / run_id / MANIFEST_NAME
        if not path.is_file():
            raise FileNotFoundError(f"no manifest for run {run_id!r} under {runs_dir}")
        return cls.model_validate_json(path.read_text(encoding="utf-8"))

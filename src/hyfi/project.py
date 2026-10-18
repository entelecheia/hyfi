"""Project paths, validated from the composed ``project`` node."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, model_validator


class Project(BaseModel):
    name: str = "hyfi-project"
    root: Path = Path()
    workspace: Path | None = None

    @model_validator(mode="after")
    def _resolve(self) -> Project:
        self.root = self.root.expanduser().resolve()
        ws = self.workspace if self.workspace is not None else Path("workspace")
        self.workspace = (self.root / ws.expanduser()).resolve()
        return self

    @property
    def runs_dir(self) -> Path:
        """Where run manifests are written."""
        return self.root / ".hyfi" / "runs"

    def path(self, *parts: str, mkdir: bool = False) -> Path:
        """A path under the workspace; ``mkdir`` creates it as a directory."""
        p = (self.workspace or self.root / "workspace").joinpath(*parts)
        if mkdir:
            p.mkdir(parents=True, exist_ok=True)
        return p

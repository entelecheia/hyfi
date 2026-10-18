"""HyFI: compose Hydra configs, validate them with Pydantic, and run reproducible workflows."""

from typing import Any

from hyfi._version import __version__
from hyfi.config import BaseConfig, compose, compose_group, instantiate, to_dict
from hyfi.manifest import RunManifest
from hyfi.project import Project
from hyfi.runner import run_workflow
from hyfi.workflow import Step, Workflow, plan

__all__ = [
    "BaseConfig",
    "Project",
    "RunManifest",
    "Step",
    "Workflow",
    "__version__",
    "compose",
    "compose_group",
    "instantiate",
    "plan",
    "run_workflow",
    "to_dict",
]

_REMOVED_1X = {"HyFI", "hyfi_main"}
MIGRATION_URL = "https://hyfi.entelecheia.ai/migration/"


def __getattr__(name: str) -> Any:
    if name in _REMOVED_1X:
        # ImportError, not AttributeError: `from hyfi import HyFI` would replace the message.
        raise ImportError(
            f"hyfi.{name} was removed in HyFI 2.0. Pin 'hyfi<2' to keep 1.x, "
            f"or see docs/migration.md ({MIGRATION_URL})."
        )
    raise AttributeError(f"module 'hyfi' has no attribute {name!r}")

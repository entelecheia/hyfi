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

_COMPAT = {"HyFI", "hyfi_main"}


def __getattr__(name: str) -> Any:
    # 1.x names load lazily so the DeprecationWarning fires on use, not on `import hyfi`.
    if name in _COMPAT:
        from hyfi import compat

        return getattr(compat, name)
    raise AttributeError(f"module 'hyfi' has no attribute {name!r}")

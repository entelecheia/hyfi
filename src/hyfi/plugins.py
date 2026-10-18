"""Discover plugin config modules through the ``hyfi.plugins`` entry point group.

A plugin declares, in its own ``pyproject.toml``::

    [project.entry-points."hyfi.plugins"]
    mypkg = "mypkg.conf"

The value is an importable package that holds Hydra config groups.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from importlib.metadata import entry_points

ENTRY_POINT_GROUP = "hyfi.plugins"


@dataclass(frozen=True)
class Plugin:
    name: str
    module: str
    distribution: str | None

    @property
    def available(self) -> bool:
        try:
            return importlib.util.find_spec(self.module) is not None
        except (ImportError, ValueError):
            return False


def discover() -> list[Plugin]:
    """Installed plugins, sorted by name so search-path order is stable."""
    found = [
        Plugin(ep.name, ep.value, ep.dist.name if ep.dist else None)
        for ep in entry_points(group=ENTRY_POINT_GROUP)
    ]
    return sorted(found, key=lambda p: p.name)


def config_modules() -> list[str]:
    """Config modules of plugins that can actually be imported."""
    return [p.module for p in discover() if p.available]

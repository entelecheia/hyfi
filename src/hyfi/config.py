"""Compose Hydra configs and validate them with Pydantic.

Nothing here runs at import time: no resolvers, no global Hydra state, no environment changes.
"""

from __future__ import annotations

import inspect
import re
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any, ClassVar, Self

from dotenv import find_dotenv, load_dotenv
from hydra import __version__ as _hydra_version
from hydra import compose as _hydra_compose
from hydra import initialize_config_dir, initialize_config_module
from hydra.core.global_hydra import GlobalHydra
from hydra.errors import ConfigCompositionException
from hydra.utils import instantiate as _hydra_instantiate
from omegaconf import DictConfig, ListConfig, OmegaConf
from pydantic import BaseModel, ConfigDict

from hyfi import plugins as _plugins

HYFI_CONFIG_MODULE = "hyfi.conf"
DEFAULT_CONFIG_DIR = "conf"
DEFAULT_CONFIG_NAME = "config"

_HYDRA_GE_14 = tuple(int(x) for x in re.findall(r"\d+", _hydra_version)[:2]) >= (1, 4)
_HYDRA_HAS_WHITELIST = "_execution_whitelist_" in inspect.signature(_hydra_instantiate).parameters


class TargetNotAllowed(PermissionError):
    """A ``_target_`` is outside the execution allowlist."""


def is_allowed(target: str, allow: Sequence[str]) -> bool:
    """Exact match, or a ``pkg.*`` pattern matching everything under ``pkg``."""
    return any(target == p or (p.endswith(".*") and target.startswith(p[:-1])) for p in allow)


def iter_targets(config: Any) -> Iterator[str]:
    """Every ``_target_`` string in a nested config."""
    data = to_dict(config, resolve=False)
    stack = [data]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if isinstance(node.get("_target_"), str):
                yield node["_target_"]
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)


def check_allowed(config: Any, allow: Sequence[str]) -> None:
    for target in iter_targets(config):
        if not is_allowed(target, allow):
            raise TargetNotAllowed(f"_target_ {target!r} is not in the execution allowlist")


def resolve_config_dir(config_dir: str | Path | None) -> Path | None:
    """The user config directory: the given one, else ``./conf`` when it exists."""
    if config_dir is not None:
        return Path(config_dir).expanduser().resolve()
    default = Path.cwd() / DEFAULT_CONFIG_DIR
    return default.resolve() if default.is_dir() else None


def search_path(
    config_dir: str | Path | None = None,
    config_name: str = DEFAULT_CONFIG_NAME,
    plugins: bool = True,
) -> tuple[str, list[str]]:
    """Return the primary config source and the extra search-path entries, highest priority first.

    The user directory is primary when it holds ``<config_name>.yaml``; otherwise ``hyfi.conf`` is
    primary and the user directory, when present, comes first among the extras. Either way the
    user directory takes precedence over plugins.
    """
    user_dir = resolve_config_dir(config_dir)
    plugin_entries = [f"pkg://{m}" for m in _plugins.config_modules()] if plugins else []
    if user_dir is not None and (user_dir / f"{config_name}.yaml").is_file():
        return f"file://{user_dir}", [*plugin_entries, f"pkg://{HYFI_CONFIG_MODULE}"]
    user_entries = [f"file://{user_dir}"] if user_dir is not None and user_dir.is_dir() else []
    return f"pkg://{HYFI_CONFIG_MODULE}", [*user_entries, *plugin_entries]


def compose(
    overrides: Sequence[str] = (),
    *,
    config_name: str = DEFAULT_CONFIG_NAME,
    config_dir: str | Path | None = None,
    plugins: bool = True,
    dotenv: bool = True,
) -> DictConfig:
    """Compose a config the way the ``hyfi`` CLI does, from code or a notebook.

    ``dotenv`` loads the nearest ``.env`` (without overriding variables already set) before
    composing, so ``${oc.env:...}`` interpolations can see it.
    """
    if dotenv:
        load_dotenv(find_dotenv(usecwd=True), override=False)
    primary, extras = search_path(config_dir, config_name, plugins)
    all_overrides = list(overrides)
    if extras:
        all_overrides.append(f"hydra.searchpath=[{','.join(extras)}]")
    # ponytail: clears any outer Hydra context (as 1.x did); nested use inside @hydra.main loses it.
    GlobalHydra.instance().clear()
    version: dict[str, Any] = {} if _HYDRA_GE_14 else {"version_base": None}
    if primary.startswith("file://"):
        init: Any = initialize_config_dir(config_dir=primary.removeprefix("file://"), **version)
    else:
        init = initialize_config_module(config_module=HYFI_CONFIG_MODULE, **version)
    with init:
        return _hydra_compose(config_name=config_name, overrides=all_overrides)


def compose_group(
    group: str,
    name: str,
    overrides: Sequence[str] = (),
    **compose_kwargs: Any,
) -> DictConfig:
    """Compose one option of a config group and return just that node."""
    group = group.strip("/")
    try:
        cfg = compose([f"{group}={name}", *overrides], **compose_kwargs)
    except ConfigCompositionException:
        cfg = compose([f"+{group}={name}", *overrides], **compose_kwargs)
    node = OmegaConf.select(cfg, group.replace("/", "."))
    if not isinstance(node, DictConfig):
        raise ValueError(f"config group {group!r} option {name!r} did not compose to a mapping")
    return node


def to_dict(cfg: Any, resolve: bool = True) -> Any:
    """Plain Python containers from a DictConfig, ListConfig, or Pydantic model."""
    if isinstance(cfg, DictConfig | ListConfig):
        return OmegaConf.to_container(cfg, resolve=resolve)
    if isinstance(cfg, BaseModel):
        return cfg.model_dump(by_alias=True)
    return cfg


def instantiate(config: Any, *args: Any, allow: Sequence[str] | None = None, **kwargs: Any) -> Any:
    """``hydra.utils.instantiate`` that also accepts Pydantic models and passes plain containers.

    A Pydantic model as ``_target_`` is validated by its own constructor. ``allow`` is an
    execution allowlist (exact targets or ``pkg.*``): every nested ``_target_`` must match it,
    and it is forwarded to Hydra's ``_execution_whitelist_`` on Hydra 1.4+.
    """
    if isinstance(config, BaseModel):
        config = config.model_dump(by_alias=True)
    kwargs.setdefault("_convert_", "all")
    if allow is not None:
        check_allowed(config, allow)
        if _HYDRA_HAS_WHITELIST:
            kwargs["_execution_whitelist_"] = list(allow)
    return _hydra_instantiate(config, *args, **kwargs)


class BaseConfig(BaseModel):
    """A Pydantic model whose defaults live in a Hydra config group.

    >>> class Tokenizer(BaseConfig):
    ...     _config_group_ = "tokenizer"
    ...     _config_name_ = "simple"
    ...     lowercase: bool = True
    >>> Tokenizer.compose(overrides=["tokenizer.lowercase=false"])  # doctest: +SKIP
    """

    model_config = ConfigDict(extra="allow")

    _config_group_: ClassVar[str | None] = None
    _config_name_: ClassVar[str] = "default"

    @classmethod
    def compose(
        cls,
        name: str | None = None,
        overrides: Sequence[str] = (),
        **compose_kwargs: Any,
    ) -> Self:
        if not cls._config_group_:
            raise TypeError(f"{cls.__name__} sets no _config_group_ to compose from")
        node = compose_group(
            cls._config_group_, name or cls._config_name_, overrides, **compose_kwargs
        )
        return cls.model_validate(to_dict(node))

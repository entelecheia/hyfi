# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy
import os
from typing import Any, Optional

from hydra import version
from hydra._internal.config_search_path_impl import ConfigSearchPathImpl
from hydra._internal.hydra import Hydra
from hydra.core.config_search_path import ConfigSearchPath
from hydra.core.global_hydra import GlobalHydra
from hydra.core.singleton import Singleton
from hydra.errors import HydraException

from hyfi.core import __hyfi_config_module_path__, __hyfi_config_path__
from hyfi.utils.logging import LOGGING
from hyfi.utils.packages import PKGs

logger = LOGGING.getLogger(__name__)


def get_gh_backup() -> Any:
    if GlobalHydra in Singleton._instances:
        return copy.deepcopy(Singleton._instances[GlobalHydra])
    else:
        return None


def restore_gh_from_backup(_gh_backup: Any) -> Any:
    if _gh_backup is None:
        del Singleton._instances[GlobalHydra]
    else:
        Singleton._instances[GlobalHydra] = _gh_backup


def get_caller_config_module_path(
    config_path: Optional[str] = __hyfi_config_path__,
) -> str:
    """Returns the path to the caller module's config folder"""
    caller_module_name = PKGs.get_caller_module_name()
    config_module = caller_module_name.split(".")[0]
    config_module_path = f"{config_module}.{config_path}"
    if config_module_path == __hyfi_config_module_path__:
        return config_module_path
    # check if the config module is importable
    try:
        __import__(config_module_path)
        return config_module_path
    except ImportError:
        logger.debug("Config module not found: %s", config_module_path)
    return ""


_UNSPECIFIED_: Any = object()


class initialize_config:
    """
    Initializes Hydra and add the config_module to the config search path.
    The config module must be importable (an __init__.py must exist at its top level)
    Optionally, a config_dir can be specified to add a file:// search path to it.

    Args:
        config_module: absolute module name, for example "hyfi.conf".
        config_dir: file system path to the config directory (default is None)
        job_name: the value for hydra.job.name (default is 'app')
    """

    def __init__(
        self,
        config_module: str,
        config_dir: Optional[str] = None,
        job_name: str = "app",
        version_base: Optional[str] = _UNSPECIFIED_,
    ) -> None:
        self._gh_backup = get_gh_backup()

        version.setbase(version_base)

        # Relative here would be interpreted as relative to cwd, which - depending on when it run
        # may have unexpected meaning. best to force an absolute path to avoid confusion.
        # Can consider using hydra.utils.to_absolute_path() to convert it at a future point if there is demand.
        if config_dir and not os.path.isabs(config_dir):
            raise HydraException(
                "initialize_config_dir() requires an absolute config_dir as input"
            )
        csp = create_config_search_path(
            config_module=config_module, search_path_dir=config_dir
        )
        Hydra.create_main_hydra2(task_name=job_name, config_search_path=csp)

    def __enter__(self, *args: Any, **kwargs: Any) -> None:
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        restore_gh_from_backup(self._gh_backup)

    def __repr__(self) -> str:
        return "hyfi.core.hydra.initialize_config()"


def append_search_path(provider: str, path: str, search_path: ConfigSearchPath) -> None:
    if not path:
        logger.debug(
            "Not adding empty path to Hydra's config search path for `%s`", provider
        )
        return
    for sp_item in search_path.get_path():
        if sp_item.path == path:
            logger.debug(
                "Not adding `%s` to Hydra's config search path, it was already added by `%s`",
                path,
                sp_item.provider,
            )
            return
    logger.debug("Adding `%s` to Hydra's config search path for `%s`", path, provider)
    search_path.append(provider, path)


def create_config_search_path(
    config_module: Optional[str],
    search_path_dir: Optional[str],
) -> ConfigSearchPath:
    from hydra.core.plugins import Plugins
    from hydra.plugins.search_path_plugin import SearchPathPlugin

    search_path = ConfigSearchPathImpl()
    search_path.append("hydra", "pkg://hydra.conf")

    # addiing hyfi's config module to the search path should come before the other modules
    append_search_path("hyfi", f"pkg://{__hyfi_config_module_path__}", search_path)

    if config_module:
        path = (
            config_module
            if config_module.startswith("pkg://")
            else f"pkg://{config_module}"
            if "." in config_module
            else ""
        )
        append_search_path("main", path, search_path)

    if caller_config_module := get_caller_config_module_path():
        append_search_path("caller", f"pkg://{caller_config_module}", search_path)

    if search_path_dir is not None and os.path.isdir(search_path_dir):
        append_search_path("user", f"file://{search_path_dir}", search_path)

    search_path_plugins = Plugins.instance().discover(SearchPathPlugin)
    for spp in search_path_plugins:
        plugin = spp()
        assert isinstance(plugin, SearchPathPlugin)
        plugin.manipulate_search_path(search_path)

    append_search_path("schema", "structured://", search_path)

    return search_path

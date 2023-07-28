"""
    HyFI: Hydra Fast Interface (Hydra and Pydantic based interface framework)

    All names of configuration folders and their counterparts folders for pydantic models
    are singular, e.g. `conf` instead of `configs`.
    All matching pydantic models are named `Config`, e.g. `BatchConfig` instead of `BatchConfigs`.

    Other module folders are plural, e.g. `utils` instead of `util`.
"""
from typing import List, Optional

from hyfi.__cli__ import hydra_main, hyfi_main
from hyfi.core import global_hyfi
from hyfi.main import HyFI
from hyfi.main import HyFI as H
from hyfi.main import HyFI as HI
from hyfi.main import global_config
from hyfi.utils.logging import LOGGING

__all__ = [
    "global_config",
    "global_hyfi",
    "hydra_main",
    "hyfi_main",
    "HyFI",
    "H",
    "HI",
    "LOGGING",
    "initialize_global_hyfi",
]


def initialize_global_hyfi(
    package_path: str,
    version: str,
    plugins: Optional[List[str]] = None,
    user_config_path: Optional[str] = None,
    config_dirname: Optional[str] = None,
) -> None:
    """
    Initializes the global HyFI instance.

    This function should be called before any other HyFI function.

    A plugin is a python module which contains a configuration module.

    Be careful!
    It does not check if the plugin is importable.

    Args:
        package_path: Path to the package root folder. e.g. `./src/hyfi`
        version: Version of the package. e.g. `0.1.0`
        plugins: A list of plugins to load. e.g. `["hyfi.conf"]`
        user_config_path: Path to the user configuration directory. e.g. `./config`
        config_dirname: Name of the configuration directory. e.g. `conf`
    """
    global_hyfi.initialize(
        package_path=package_path,
        version=version,
        plugins=plugins,
        user_config_path=user_config_path,
        config_dirname=config_dirname,
    )

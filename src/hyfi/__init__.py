"""
    HyFI: Hydra Fast Interface (Hydra and Pydantic based interface framework)

    All names of configuration folders and their counterparts folders for pydantic models
    are singular, e.g. `conf` instead of `configs`.
    All matching pydantic models are named `Config`, e.g. `BatchConfig` instead of `BatchConfigs`.

    Other module folders are plural, e.g. `utils` instead of `util`.
"""
from hyfi.__cli__ import hydra_main, hyfi_main
from hyfi.core import __global_hyfi__ as global_hyfi
from hyfi.core import __hydra_version_base__
from hyfi.core.config import __global_config__ as global_config
from hyfi.main import HyFI
from hyfi.main import HyFI as H
from hyfi.main import HyFI as HI
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
    "__hydra_version_base__",
]


def initialize_global_hyfi(
    package_name: str,
    version: str,
) -> None:
    """
    Initializes the global HyFI instance.

    This function should be called before any other HyFI function.
    """
    global_hyfi.initialize(package_name=package_name, version=version)

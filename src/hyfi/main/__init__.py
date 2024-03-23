"""
This module serves as the entry point for the HyFI application.

It imports the necessary classes and objects from the 'config' and 'main' modules,
and defines the '__all__' list to specify the public interface of this module.

Classes:
- GlobalConfig: Represents the global configuration for the HyFI application.
- GlobalConfigResolver: Resolves the global configuration for the HyFI application.
- HyFIConfig: Represents the configuration for the HyFI application.
- HyFI: Represents the main class of the HyFI application.

Objects:
- global_config: An instance of the GlobalConfig class representing the global configuration.

"""

from .config import GlobalConfig, GlobalConfigResolver, HyFIConfig, global_config
from .main import HyFI

__all__ = [
    "GlobalConfig",
    "GlobalConfigResolver",
    "global_config",
    "HyFI",
    "HyFIConfig",
]

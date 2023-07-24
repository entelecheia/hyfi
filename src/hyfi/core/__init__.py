"""
    HyFI Core Module
"""
import importlib
import os
from pathlib import Path
from typing import Any, List, Optional

from pydantic import BaseModel

from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

__hydra_version_base__ = "1.2"
__hydra_default_config_group_value__ = "__init__"
__hyfi_name__: str = "HyFI"
__hyfi_config_path__ = "conf"
__hyfi_config_name__ = "config"
__hyfi_package_name__: str = "hyfi"
__hyfi_package_path__: str = Path(__file__).parent.parent.as_posix()
__hyfi_config_module_path__ = f"{__hyfi_package_name__}.{__hyfi_config_path__}"

_batcher_instance_ = None


def __hyfi_version__() -> str:
    """
    Returns the version of HyFI.

    Returns:
        string containing the version of HyFI
    """
    from hyfi._version import __version__

    return __version__


class GlobalHyFIConfig(BaseModel):
    """Global configuration for HyFI

    Attributes:
    __package_name__ (str): The name of the package.
    __package_path__ (str): The path to the package root folder.
    __config_name__ (str): The name of the configuration module.
    __config_path__ (str): The path to the configuration module.
    __user_config_path__ (str): The path to the user configuration directory.
    __plugins__ (List[Any]): A list of plugins to load.
    __version__ (str): The version number of the package.
    """

    __package_name__: str = __hyfi_package_name__
    __package_path__: str = __hyfi_package_path__
    __config_name__: str = __hyfi_config_name__
    __config_path__: str = __hyfi_config_path__
    __user_config_path__: str = "config"
    __plugins__: Optional[List[str]] = None
    __version__: str = __hyfi_version__()

    def initialize(
        self,
        package_name: str = __hyfi_name__,
        version: str = __hyfi_version__(),
        plugins: Optional[List[str]] = None,
    ) -> None:
        """
        Initializes the global HyFI instance.
        """
        self.__package_name__ = package_name
        self.__version__ = version
        if plugins:
            self.__plugins__ = self.get_plugins(plugins)

    @property
    def plugins(self) -> Optional[List[str]]:
        """Returns the list of plugins to load."""
        return self.__plugins__

    def get_plugins(self, plugins: List[str]) -> List[str]:
        """Returns the list of plugins to load."""
        _plugins = []
        for plugin in plugins:
            H = self._safe_import_module(plugin)
            if H and getattr(H, "config_module", None):
                _plugins.append(H.config_module)
        return _plugins

    @staticmethod
    def _safe_import_module(module_name: str) -> Any:
        """Safely imports a module."""
        try:
            return importlib.import_module(module_name).HyFI
        except ImportError:
            logger.debug("Failed to import module: %s", module_name)
            return None

    @property
    def version(self) -> str:
        """Returns the version number of the package."""
        return self.__version__

    @property
    def config_module(self) -> str:
        """Returns the name of the configuration module."""
        return f"{self.__package_name__}.{self.__config_path__}"

    @property
    def config_module_path(self) -> str:
        """Returns the path to the configuration module."""
        return f"pkg://{self.config_module}"

    @property
    def config_name(self) -> str:
        """Returns the name of the configuration module."""
        return self.__config_name__

    @property
    def user_config_path(self) -> str:
        """Returns the path to the user configuration directory."""
        # if user_config_path is not an absolute path, make it absolute
        search_path = self.__user_config_path__
        if not os.path.isdir(search_path):
            search_path = os.environ.get("HYFI_USER_CONFIG_PATH", "")
        if os.path.isdir(search_path):
            self.__user_config_path__ = (
                search_path
                if os.path.isabs(search_path)
                else os.path.join(os.getcwd(), search_path)
            )
        else:
            logger.debug(
                "The user configuration directory does not exist: %s", search_path
            )
            self.__user_config_path__ = ""
        return self.__user_config_path__

    @property
    def hyfi_config_module_path(self) -> str:
        """Returns the path to the HyFI root folder"""
        return self.config_module_path

    @property
    def hyfi_config_module(self) -> str:
        """Returns the name of the configuration module."""
        return self.config_module

    @property
    def hyfi_user_config_path(self) -> str:
        """Returns the path to the user configuration directory."""
        return self.user_config_path

    @property
    def hyfi_config_name(self) -> str:
        """Returns the name of the configuration module."""
        return self.config_name


__global_hyfi__ = GlobalHyFIConfig()


def __hyfi_path__():
    """Returns the path to the HyFI root folder"""
    return Path(__file__).parent.parent.as_posix()


def __home_path__():
    """Returns the path to the user's home folder"""
    return Path.home().as_posix()


def __app_version__() -> str:
    """
    Returns the version of App.

    Returns:
        string containing the version of App
    """

    return __global_hyfi__.version


def __package_name__() -> str:
    """
    Returns the package name of the App

    Returns:
        string containing the package name of the App
    """

    return __global_hyfi__.__package_name__


def __package_path__() -> str:
    """
    Returns the path to the App root folder

    Returns:
        string containing the path to the App root folder
    """

    return __global_hyfi__.__package_path__

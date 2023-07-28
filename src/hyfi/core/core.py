"""
    HyFI Core Module
"""
import os
from pathlib import Path
from typing import List, Optional, Set, Tuple

from pydantic import BaseModel

from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

__hydra_version_base__: str = "1.2"
__hydra_default_config_group_value__: str = "__init__"
__hyfi_name__: str = "HyFI"
__hyfi_config_dirname__: str = "conf"
__hyfi_config_name__: str = "config"
__hyfi_user_config_path__: str = "config"
__hyfi_package_path__: str = Path(__file__).parent.parent.as_posix()
__hyfi_package_name__: str = os.path.basename(__hyfi_package_path__)
__hyfi_config_module__: str = f"{__hyfi_package_name__}.{__hyfi_config_dirname__}"
__hyfi_config_module_path__: str = f"pkg://{__hyfi_config_module__}"
__global_package_list__: Set[str] = {"cmd", "mode", "workflow"}

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
    __version__ (str): The version number of the package.
    __plugins__ (List[Any]): A list of plugins to load.
    __config_name__ (str): The name of the configuration module.
    __config_dirname__ (str): The name of the configuration directory.
    __user_config_path__ (str): The path to the user configuration directory.
    """

    __package_name__: str = __hyfi_package_name__
    __package_path__: str = __hyfi_package_path__
    __version__: str = __hyfi_version__()
    __plugins__: Optional[List[str]] = None

    __config_name__: str = __hyfi_config_name__
    __config_dirname__: str = __hyfi_config_dirname__
    __user_config_path__: str = __hyfi_user_config_path__

    _packages_: List[Tuple[str, str]] = [(__hyfi_package_path__, __hyfi_version__())]

    def initialize(
        self,
        package_path: str = __hyfi_name__,
        version: str = __hyfi_version__(),
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
        self.__package_path__ = package_path
        self.__version__ = version
        if package_path not in self._packages_:
            self._packages_.append((package_path, version))
        if plugins:
            self.__plugins__ = self.get_plugins(plugins)
        if user_config_path:
            self.__user_config_path__ = user_config_path
        if config_dirname:
            self.__config_dirname__ = config_dirname

    @property
    def plugins(self) -> Optional[List[str]]:
        """Returns the list of plugins to load."""
        return self.__plugins__

    def get_plugins(self, plugins: List[str]) -> List[str]:
        """Returns the list of plugins to load.
        A plugin is a python module which contains a configuration module.

        Be careful!
        It does not check if the plugin is importable.

        Args:
            plugins: List[str]: A list of plugins to load.
        """
        _plugins = []
        for plugin in plugins:
            plugin = plugin.split(".")[0]
            config_module = f"{plugin}.{self.__config_dirname__}"
            _plugins.append(config_module)
        return _plugins

    @property
    def package_name(self) -> str:
        """Returns the name of the package."""
        self.__package_name__ = os.path.basename(self.package_path)
        return self.__package_name__

    @property
    def package_path(self) -> str:
        """Returns the path to the package root folder.

        If there are multiple packages, the second package is returned.
        If there is only one package, the first package is returned. (default: hyfi)
        """
        if len(self._packages_) > 1:
            self.__package_path__ = self._packages_[1][0]
        else:
            self.__package_path__ = self._packages_[0][0]
        return self.__package_path__

    @property
    def version(self) -> str:
        """Returns the version number of the package."""
        if len(self._packages_) > 1:
            self.__version__ = self._packages_[1][1]
        else:
            self.__version__ = self._packages_[0][1]
        return self.__version__

    @property
    def config_dirname(self) -> str:
        """Returns the name of the configuration directory."""
        return self.__config_dirname__

    @property
    def config_root(self) -> str:
        """Returns the path to the configuration root directory."""
        return f"{self.package_path}/{self.config_dirname}"

    @property
    def config_module(self) -> str:
        """Returns the name of the configuration module."""
        return f"{self.package_name}.{self.config_dirname}"

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
    def hyfi_name(self) -> str:
        """Returns the name of HyFI package."""
        return __hyfi_name__

    @property
    def hyfi_config_module_path(self) -> str:
        """Returns the path to HyFI root folder"""
        return __hyfi_config_module_path__

    @property
    def hyfi_config_module(self) -> str:
        """Returns the name of HyFI default configuration module."""
        return __hyfi_config_module__

    @property
    def hyfi_config_name(self) -> str:
        """Returns the name of HyFI default configuration module."""
        return __hyfi_config_name__

    @property
    def hyfi_config_dirname(self) -> str:
        """Returns the name of HyFI default configuration directory."""
        return __hyfi_config_dirname__

    @property
    def hyfi_package_name(self) -> str:
        """Returns the name of HyFI package."""
        return __hyfi_package_name__

    @property
    def hyfi_package_path(self) -> str:
        """Returns the path to the package root folder."""
        return __hyfi_package_path__

    @property
    def hydra_version_base(self) -> str:
        """Returns the version of Hydra."""
        return __hydra_version_base__

    @property
    def hydra_default_config_group_value(self) -> str:
        """Returns the default config group value of Hydra."""
        return __hydra_default_config_group_value__

    @property
    def global_package_list(self) -> Set[str]:
        """Returns the list of global packages."""
        return __global_package_list__


__global_hyfi__ = GlobalHyFIConfig()


def __hyfi_path__() -> str:
    """Returns the path to the HyFI root folder"""
    return __global_hyfi__.hyfi_package_path


def __home_path__() -> str:
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

    return __global_hyfi__.package_name


def __package_path__() -> str:
    """
    Returns the path to the App root folder

    Returns:
        string containing the path to the App root folder
    """

    return __global_hyfi__.package_path


def __config_module_path__() -> str:
    """Global HyFI config path for the package to search for."""
    return __global_hyfi__.config_module_path


def __user_config_path__() -> str:
    """Global HyFI user config path for the package to search for."""
    return __global_hyfi__.user_config_path

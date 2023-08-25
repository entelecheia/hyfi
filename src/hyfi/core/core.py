"""
    HyFI Core Module
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from pydantic import BaseModel

from hyfi.utils.logging import LOGGING
from hyfi.utils.packages import PKGs

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
    __dotenv_file__ (str): The name of the dotenv file.
    __secrets_dir__ (str): The name of the secrets directory.
    """

    __package_name__: str = __hyfi_package_name__
    __package_path__: str = __hyfi_package_path__
    __version__: str = __hyfi_version__()
    __plugins__: Optional[Dict[str, List[str]]] = None

    __config_name__: str = __hyfi_config_name__
    __config_dirname__: str = __hyfi_config_dirname__
    __user_config_path__: str = __hyfi_user_config_path__

    __dotenv_file__: str = ".env"
    __secrets_dir__: str = "./secrets"

    __verbosity__: Union[bool, int] = False

    _packages_: List[Tuple[str, str]] = [(__hyfi_package_path__, __hyfi_version__())]

    def initialize(
        self,
        package_path: str = __hyfi_name__,
        version: str = __hyfi_version__(),
        plugins: Optional[List[str]] = None,
        user_config_path: Optional[str] = None,
        config_dirname: Optional[str] = None,
        dotenv_file: Optional[str] = None,
        secrets_dir: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Initializes the global HyFI instance.
        This function should be called before any other HyFI function.
        A plugin is a python module which contains a configuration module.

        Args:
            package_path: Path to the package root folder. e.g. `./src/hyfi`
            version: Version of the package. e.g. `0.1.0`
            plugins: A list of plugins to load. e.g. `["hyfi.conf"]`
            user_config_path: Path to the user configuration directory. e.g. `./config`
            config_dirname: Name of the configuration directory. e.g. `conf`
            dotenv_file: Name of the dotenv file. e.g. `.env`
            secrets_dir: Name of the secrets directory. e.g. `secrets`
            **kwargs: Additional arguments to be set as attributes.
        """
        self.__package_path__ = package_path
        self.__version__ = version
        if package_path not in self._packages_:
            self._packages_.append((package_path, version))
        if plugins:
            self.__plugins__ = self.init_plugins(plugins)
        if user_config_path:
            self.__user_config_path__ = user_config_path
        if config_dirname:
            self.__config_dirname__ = config_dirname
        if dotenv_file:
            self.__dotenv_file__ = dotenv_file
        if secrets_dir:
            self.__secrets_dir__ = secrets_dir

        # for the future use
        for key, value in kwargs.items():
            key_name = (
                key if key.startswith("__") and key.endswith("__") else f"__{key}__"
            )
            if hasattr(self, key_name):
                setattr(self, key, value)
            else:
                logger.warning("Invalid key: %s", key)

    def reinitialize(
        self,
        plugins: Optional[List[str]] = None,
        user_config_path: Optional[str] = None,
        dotenv_file: Optional[str] = None,
        secrets_dir: Optional[str] = None,
    ) -> None:
        """
        Re-initializes the global HyFI instance.

        Args:
            plugins: A list of plugins to load. e.g. `["hyfi.conf"]`
            user_config_path: Path to the user configuration directory. e.g. `./config`
            dotenv_file: Name of the dotenv file. e.g. `.env`
            secrets_dir: Name of the secrets directory. e.g. `secrets`
        """
        if plugins:
            self.__plugins__ = self.init_plugins(plugins)
        if user_config_path:
            self.__user_config_path__ = user_config_path
        if dotenv_file:
            self.__dotenv_file__ = dotenv_file
        if secrets_dir:
            self.__secrets_dir__ = secrets_dir

    @property
    def dotenv_file(self) -> str:
        """Returns the name of the dotenv file."""
        if os.environ.get("DOTENV_FILE"):
            return os.environ.get("DOTENV_FILE")
        return self.__dotenv_file__

    @property
    def secrets_dir(self) -> str:
        """Returns the path of the secrets directory."""
        secret_dir = self.__secrets_dir__
        if not os.path.isdir(secret_dir):
            secret_dir = os.environ.get("HYFI_SECRETS_DIR", "")
        if os.path.isdir(secret_dir):
            secret_dir = (
                secret_dir
                if os.path.isabs(secret_dir)
                else os.path.join(os.getcwd(), secret_dir)
            )
        else:
            logger.debug("The secrets directory does not exist.")
            secret_dir = None
        return secret_dir

    @property
    def plugins(self) -> Optional[List[str]]:
        """Returns the list of plugins to load."""
        if self.__plugins__:
            caller_pkg_name = PKGs.get_next_level_caller_package_name()
            if caller_pkg_name in self.__plugins__:
                logger.debug(
                    "Loading plugins for %s: %s",
                    caller_pkg_name,
                    self.__plugins__[caller_pkg_name],
                )
                return self.__plugins__[caller_pkg_name]
        return None

    def init_plugins(self, plugins: List[str]) -> Dict[str, List[str]]:
        """Returns the list of plugins to load.
        A plugin is a python module which contains a configuration module.

        Args:
            plugins: List[str]: A list of plugins to load.

        Returns:
            Dict[str, List[str]]: A dictionary of plugins to load. ex) plugins = {'__package_name__': ['plugin1.conf', 'plugin2.conf']}
        """
        caller_pkg_name = PKGs.get_next_level_caller_package_name()
        _plugins = []
        for plugin in plugins:
            plugin = plugin.split(".")[0]
            if PKGs.is_importable(plugin):
                logger.debug("Plugin %s is importable.", plugin)
                config_module = f"{plugin}.{self.__config_dirname__}"
            else:
                logger.debug("Plugin %s is not importable.", plugin)
            _plugins.append(config_module)
        return {caller_pkg_name: _plugins}

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

    @property
    def verbosity(self) -> int:
        """Returns the verbosity level."""
        if os.environ.get("HYFI_VERBOSITY"):
            self.__verbosity__ = int(os.environ.get("HYFI_VERBOSITY", 0))
        return self.__verbosity__


__global_hyfi__ = GlobalHyFIConfig()


class GlobalHyFIResolver:
    @staticmethod
    def __hyfi_version__() -> str:
        """
        Returns the version of HyFI.

        Returns:
            string containing the version of HyFI
        """
        from hyfi._version import __version__

        return __version__

    def __hyfi_path__() -> str:
        """Returns the path to the HyFI root folder"""
        return __global_hyfi__.hyfi_package_path

    @staticmethod
    def __home_path__() -> str:
        """Returns the path to the user's home folder"""
        return Path.home().as_posix()

    @staticmethod
    def __app_version__() -> str:
        """
        Returns the version of App.

        Returns:
            string containing the version of App
        """

        return __global_hyfi__.version

    @staticmethod
    def __package_name__() -> str:
        """
        Returns the package name of the App

        Returns:
            string containing the package name of the App
        """

        return __global_hyfi__.package_name

    @staticmethod
    def __package_path__() -> str:
        """
        Returns the path to the App root folder

        Returns:
            string containing the path to the App root folder
        """

        return __global_hyfi__.package_path

    @staticmethod
    def __config_module_path__() -> str:
        """Global HyFI config path for the package to search for."""
        return __global_hyfi__.config_module_path

    @staticmethod
    def __user_config_path__() -> str:
        """Global HyFI user config path for the package to search for."""
        return __global_hyfi__.user_config_path

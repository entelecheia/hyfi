"""This module contains the About Configuration for the HyFI package.

It defines the AboutConfig class, which is a Pydantic BaseModel that contains
metadata about the package, such as its name, version, authors, and license.
It also defines the model_config attribute, which is a ConfigDict that allows
extra configuration options to be added to the AboutConfig instance.
"""
import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

__hyfi_package_name__: str = "hyfi"
__hyfi_package_path__: str = Path(__file__).parent.parent.as_posix()
__hyfi_name__: str = "HyFI"
__hyfi_authors__: str = "Young Joon Lee <entelecheia@hotmail.com>"
__hyfi_description__: str = (
    "Hydra Fast Interface (Hydra and Pydantic based interface framework)"
)
__hyfi_homepage__: str = "https://hyfi.entelecheia.ai"
__hyfi_license__: str = "MIT"


def __hyfi_version__() -> str:
    """
    Returns the version of HyFI.

    Returns:
        string containing the version of HyFI
    """
    from hyfi._version import __version__

    return __version__


class AboutConfig(BaseModel):
    """A Pydantic BaseModel that contains metadata about the package.

    Attributes:
        __package_name__ (str): The name of the package.
        __user_config_path__ (str): The path to the user configuration directory.
        name (str): The display name of the package.
        authors (str): The author(s) of the package.
        description (str): A brief description of the package.
        homepage (str): The URL of the package's homepage.
        license (str): The license under which the package is distributed.
        version (str): The version number of the package.
        model_config (ConfigDict): A ConfigDict that allows extra configuration
            options to be added to the AboutConfig instance.
    """

    _config_group_: str = "about"
    __package_name__: str = __hyfi_package_name__
    __package_path__: str = __hyfi_package_path__
    __user_config_path__: str = "config"
    __version__: str = __hyfi_version__()

    name: str = __hyfi_name__
    authors: str = __hyfi_authors__
    description: str = __hyfi_description__
    homepage: str = __hyfi_homepage__
    license: str = __hyfi_license__
    version: str = __hyfi_version__()

    model_config = ConfigDict(extra="allow")  # type: ignore

    @property
    def config_module(self) -> str:
        """Returns the name of the configuration module."""
        return f"{self.__package_name__}.conf"

    @property
    def config_path(self) -> str:
        """Returns the path to the configuration module."""
        return f"pkg://{self.config_module}"

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

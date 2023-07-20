"""This module contains the About Configuration for the HyFI package.

It defines the AboutConfig class, which is a Pydantic BaseModel that contains
metadata about the package, such as its name, version, authors, and license.
It also defines the model_config attribute, which is a ConfigDict that allows
extra configuration options to be added to the AboutConfig instance.
"""
import os

from pydantic import BaseModel, ConfigDict

from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

__package_name__: str = "hyfi"
__app_name__: str = "HyFI"
__authors__: str = "Young Joon Lee <entelecheia@hotmail.com>"
__description__: str = (
    "Hydra Fast Interface (Hydra and Pydantic based interface framework)"
)
__homepage__: str = "https://hyfi.entelecheia.ai"
__license__: str = "MIT"


def __version__() -> str:
    """
    Returns the version of Hyfi. It is used to determine the version of Hyfi.


    Returns:
        string containing the version of
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
    __package_name__: str = __package_name__
    __user_config_path__: str = "config"

    name: str = __app_name__
    authors: str = __authors__
    description: str = __description__
    homepage: str = __homepage__
    license: str = __license__
    version: str = __version__()

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
        if not os.path.isabs(self.__user_config_path__):
            self.__user_config_path__ = os.path.join(
                os.getcwd(), self.__user_config_path__
            )
        return self.__user_config_path__

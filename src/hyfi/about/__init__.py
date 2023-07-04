"""This module contains the About Configuration for the HyFI package.

It defines the AboutConfig class, which is a Pydantic BaseModel that contains
metadata about the package, such as its name, version, authors, and license.
It also defines the model_config attribute, which is a ConfigDict that allows
extra configuration options to be added to the AboutConfig instance.
"""
from pydantic import BaseModel, ConfigDict

from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class AboutConfig(BaseModel):
    """A Pydantic BaseModel that contains metadata about the package.

    Attributes:
        __package_name__ (str): The name of the package.
        name (str): The display name of the package.
        authors (str): The author(s) of the package.
        description (str): A brief description of the package.
        homepage (str): The URL of the package's homepage.
        license (str): The license under which the package is distributed.
        version (str): The version number of the package.
        model_config (ConfigDict): A ConfigDict that allows extra configuration
            options to be added to the AboutConfig instance.
    """

    __package_name__: str = "hyfi"
    name: str = "HyFI"
    authors: str = "Young Joon Lee <entelecheia@hotmail.com>"
    description: str = (
        "Hydra Fast Interface (Hydra and Pydantic based interface framework)"
    )
    homepage: str = "https://hyfi.entelecheia.ai"
    license: str = "MIT"
    version: str = "0.0.0"

    model_config = ConfigDict(extra="allow")  # type: ignore

    @property
    def config_module(self) -> str:
        """Returns the name of the configuration module."""
        return f"{self.__package_name__}.conf"

    @property
    def config_path(self) -> str:
        """Returns the path to the configuration module."""
        return f"pkg://{self.config_module}"

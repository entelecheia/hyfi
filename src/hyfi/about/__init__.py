"""This module contains the About Configuration for the HyFI package.

It defines the AboutConfig class, which is a Pydantic BaseModel that contains
metadata about the package, such as its name, version, authors, and license.
It also defines the model_config attribute, which is a ConfigDict that allows
extra configuration options to be added to the AboutConfig instance.
"""
from hyfi.composer import BaseModel, ConfigDict
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

__hyfi_name__: str = "HyFI"
__hyfi_authors__: str = "Young Joon Lee <entelecheia@hotmail.com>"
__hyfi_description__: str = (
    "Hydra Fast Interface (Hydra and Pydantic based interface framework)"
)
__hyfi_homepage__: str = "https://hyfi.entelecheia.ai"
__hyfi_license__: str = "MIT"


class AboutConfig(BaseModel):
    """A Pydantic BaseModel that contains metadata about the package.

    Attributes:
        name (str): The display name of the package.
        authors (str): The author(s) of the package.
        description (str): A brief description of the package.
        homepage (str): The URL of the package's homepage.
        license (str): The license under which the package is distributed.
    """

    _config_group_: str = "about"

    name: str = __hyfi_name__
    authors: str = __hyfi_authors__
    description: str = __hyfi_description__
    homepage: str = __hyfi_homepage__
    license: str = __hyfi_license__

    model_config = ConfigDict(extra="allow")  # type: ignore

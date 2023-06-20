from pydantic import BaseModel

from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


class AboutConfig(BaseModel):
    """About Configuration"""

    __package_name__: str = "hyfi"
    name: str = "HyFI"
    authors: str = "Young Joon Lee <entelecheia@hotmail.com>"
    description: str = (
        "Hydra Fast Interface (Hydra and Pydantic based interface framework)"
    )
    homepage: str = "https://hyfi.entelecheia.ai"
    license: str = "MIT"
    version: str = "0.0.0"

    class Config:
        extra = "allow"
        underscore_attrs_are_private = False

    @property
    def config_module(self) -> str:
        return f"{self.__package_name__}.conf"

    @property
    def config_path(self) -> str:
        return f"pkg://{self.config_module}"

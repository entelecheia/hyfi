from pathlib import Path

from pydantic import BaseModel

from hyfi.about import AboutConfig
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)

__hydra_version_base__ = "1.2"
__hydra_default_config_group_value__ = "default"

__about__ = AboutConfig()


class HydraConfig(BaseModel):
    """HyFI config primary class"""

    hyfi_config_path: str = __about__.config_path
    hyfi_config_module: str = __about__.config_module
    hyfi_user_config_path: str = ""


__hydra_config__ = HydraConfig()


def __hyfi_path__():
    return Path(__file__).parent.parent.as_posix()


def __home_path__():
    return Path.home().as_posix()

from pathlib import Path

from pydantic import BaseModel

from hyfi.about import AboutConfig, __package_name__
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

__hydra_version_base__ = "1.2"
__hydra_default_config_group_value__ = "__init__"
__config_path__ = "conf"
__config_name__ = "config"
__config_module_path__ = f"{__package_name__}.{__config_path__}"

__about__ = AboutConfig()
_batcher_instance_ = None


class HydraConfig(BaseModel):
    """Global configuration for Hydra"""

    hyfi_config_path: str = __about__.config_path
    hyfi_config_module: str = __about__.config_module
    hyfi_user_config_path: str = __about__.user_config_path


__hydra_config__ = HydraConfig()


def __hyfi_path__():
    """Returns the path to the HyFI root folder"""
    return Path(__file__).parent.parent.as_posix()


def __home_path__():
    """Returns the path to the user's home folder"""
    return Path.home().as_posix()

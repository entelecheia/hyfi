from pathlib import Path

from pydantic import BaseModel

from hyfi.about import AboutConfig, __hyfi_package_name__
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

__hydra_version_base__ = "1.2"
__hydra_default_config_group_value__ = "__init__"
__config_path__ = "conf"
__config_name__ = "config"
__hyfi_config_module_path__ = f"{__hyfi_package_name__}.{__config_path__}"

__about__ = AboutConfig()
_batcher_instance_ = None


def __app_name__() -> str:
    """
    Returns the name of the App

    Returns:
        string containing the name of the App
    """

    return __about__.name


def __app_version__() -> str:
    """
    Returns the version of App.

    Returns:
        string containing the version of App
    """

    return __about__.__version__


def __package_name__() -> str:
    """
    Returns the package name of the App

    Returns:
        string containing the package name of the App
    """

    return __about__.__package_name__


def __package_path__() -> str:
    """
    Returns the path to the App root folder

    Returns:
        string containing the path to the App root folder
    """

    return __about__.__package_path__


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

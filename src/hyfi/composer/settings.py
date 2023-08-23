"""
HyFI Base Settings Class
"""
import os
from typing import Optional, Tuple, Type

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import DotEnvSettingsSource as PydanticDotEnvSettingsSource
from pydantic_settings import PydanticBaseSettingsSource, SettingsConfigDict
from pydantic_settings.sources import ENV_FILE_SENTINEL, DotenvType

from hyfi.composer import model_validator
from hyfi.core import global_hyfi
from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class DotEnvSettingsSource(PydanticDotEnvSettingsSource):
    def __init__(
        self,
        settings_cls: PydanticBaseSettings,
        env_file: Optional[DotenvType] = ENV_FILE_SENTINEL,
        env_file_encoding: Optional[str] = None,
        case_sensitive: Optional[bool] = None,
        env_prefix: Optional[str] = None,
        env_nested_delimiter: Optional[str] = None,
    ) -> None:
        env_file = (
            env_file
            if env_file != ENV_FILE_SENTINEL
            else settings_cls.model_config.get("env_file")
        )
        self.env_file = ENVs.find_dotenv(env_file) or env_file
        if os.path.isfile(self.env_file):
            os.environ["DOTENV_FILE"] = self.env_file
            logger.debug("found dotenv file: %s", self.env_file)
        else:
            logger.debug("dotenv file not found: %s", self.env_file)
        self.env_file_encoding = (
            env_file_encoding
            if env_file_encoding is not None
            else settings_cls.model_config.get("env_file_encoding")
        )
        super().__init__(
            settings_cls,
            env_file,
            env_file_encoding,
            case_sensitive,
            env_prefix,
            env_nested_delimiter,
        )


class BaseSettings(PydanticBaseSettings, ENVs):
    """
    Configuration class for environment variables in HyFI.

    !! The variables are read-only and cannot be changed after initialization.
    """

    """Environment variables for HyFI"""

    _config_name_: str = "__init__"
    _config_group_: str = "/env"

    DOTENV_FILENAME: Optional[str] = ".env"
    DOTENV_DIR: Optional[str] = None
    DOTENV_FILE: Optional[str] = None
    HYFI_SECRETS_DIR: Optional[str] = None

    model_config = SettingsConfigDict(
        env_prefix="",
        env_nested_delimiter="__",
        case_sentive=False,
        env_file=global_hyfi.dotenv_file,
        env_file_encoding="utf-8",
        validate_assignment=True,
        extra="allow",
        secrets_dir=global_hyfi.secrets_dir,
    )  # type: ignore

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[PydanticBaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        # BaseSettings.load_dotenv(dotenv_file=global_hyfi.dotenv_file)
        return (
            init_settings,
            file_secret_settings,
            DotEnvSettingsSource(settings_cls),
            env_settings,
        )

    @model_validator(mode="before")  # type: ignore
    def check_and_set_values(cls, data):
        if not isinstance(data, dict):
            return data
        env_file = os.environ.get("DOTENV_FILE", "")
        if os.path.isfile(env_file):
            data["DOTENV_FILE"] = env_file
            dotenv_filename = os.path.basename(env_file)
            dotenv_dir = os.path.dirname(env_file)
            data["DOTENV_DIR"] = dotenv_dir
            data["DOTENV_FILENAME"] = dotenv_filename
        data["HYFI_SECRETS_DIR"] = global_hyfi.secrets_dir
        return BaseSettings.check_and_set_osenv_vars(data)

    @property
    def os(self):
        """Returns the OS environment variables."""
        return os.environ

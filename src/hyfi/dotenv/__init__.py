import os
from typing import Optional, Tuple, Union

from pydantic import BaseSettings, Field, SecretStr, root_validator
from pydantic.env_settings import SettingsSourceCallable

from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class DotEnvConfig(BaseSettings):
    """Environment variables for HyFI"""

    _config_name_: str = "__init__"

    DOTENV_FILENAME: Optional[str] = ".env"
    DOTENV_DIR: Optional[str] = ""
    DOTENV_PATH: Optional[str] = ""
    # Internal
    HYFI_RESOURCE_DIR: Optional[str] = ""
    HYFI_GLOBAL_ROOT: Optional[str] = ""
    HYFI_GLOBAL_WORKSPACE_NAME: Optional[str] = "workspace"
    HYFI_PROJECT_NAME: Optional[str] = ""
    HYFI_PROJECT_DESC: Optional[str] = ""
    HYFI_PROJECT_ROOT: Optional[str] = ""
    HYFI_PROJECT_WORKSPACE_NAME: Optional[str] = "workspace"
    HYFI_LOG_LEVEL: Optional[str] = "WARNING"
    HYFI_VERBOSE: Optional[Union[bool, str, int]] = False
    HYFI_NUM_WORKERS: Optional[int] = 1
    CACHED_PATH_CACHE_ROOT: Optional[str] = ""
    # For other packages
    CUDA_DEVICE_ORDER: Optional[str] = "PCI_BUS_ID"
    CUDA_VISIBLE_DEVICES: Optional[str] = ""
    WANDB_PROJECT: Optional[str] = ""
    WANDB_DISABLED: Optional[str] = ""
    WANDB_DIR: Optional[str] = ""
    WANDB_NOTEBOOK_NAME: Optional[str] = ""
    WANDB_SILENT: Optional[Union[bool, str]] = False
    LABEL_STUDIO_SERVER: Optional[str] = ""
    KMP_DUPLICATE_LIB_OK: Optional[str] = "True"
    TOKENIZERS_PARALLELISM: Optional[Union[bool, str]] = False
    # API Keys and Tokens
    WANDB_API_KEY: Optional[SecretStr] = Field(exclude=True)
    HUGGING_FACE_HUB_TOKEN: Optional[SecretStr] = Field(exclude=True)
    OPENAI_API_KEY: Optional[SecretStr] = Field(exclude=True)
    ECOS_API_KEY: Optional[SecretStr] = Field(exclude=True)
    FRED_API_KEY: Optional[SecretStr] = Field(exclude=True)
    NASDAQ_API_KEY: Optional[SecretStr] = Field(exclude=True)
    HF_USER_ACCESS_TOKEN: Optional[SecretStr] = Field(exclude=True)
    LABEL_STUDIO_USER_TOKEN: Optional[SecretStr] = Field(exclude=True)

    class Config:
        env_prefix = ""
        env_nested_delimiter = "__"
        case_sentive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        validate_assignment = True
        extra = "allow"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            ENVs.load_dotenv()
            return env_settings, file_secret_settings, init_settings

    @root_validator()
    def check_and_set_values(cls, values):
        return ENVs.check_and_set_osenv_vars(values)

    @property
    def os(self):
        return os.environ

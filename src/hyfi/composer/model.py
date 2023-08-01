"""
    HiFY Base Model Class
"""
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, model_validator

from hyfi.core import global_hyfi
from hyfi.utils.logging import LOGGING

from .composer import Composer

logger = LOGGING.getLogger(__name__)

__all__ = ["BaseModel", "model_validator"]


class BaseModel(PydanticBaseModel):
    """
    Base class for all Pydantic models.
    """

    _config_name_: str = "__init__"
    _config_group_: str = ""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=False,
    )  # type: ignore

    @classmethod
    def save_hyfi_config(
        cls,
        config_name: Optional[str] = None,
        config_path: str = None,
        config_root: Optional[str] = None,
        **kwargs_for_target,
    ) -> Dict[str, Any]:
        """
        Saves a HyFI config for itself.

        Args:
            cls (BaseModel): The class to generate a config for.
            config_name (Optional[str]): The name of the config. If not provided, the name of the target will be used.
            config_path (Optional[str]): The path to save the config to (relative to the config root). Defaults to "run".
            config_root (Optional[str]): The root of the config path. If not provided, the global hyfi config directory will be used.
            **kwargs_for_target: Keyword arguments to pass to the target.
        """

        target = f"{cls.__module__}.{cls.__name__}"
        cfg = {
            "_target_": target,
            "_config_name_": getattr(cls._config_name_, "default"),
            "_config_group_": getattr(cls._config_group_, "default"),
        }

        model_fields = {
            key: getattr(value, "default") for key, value in cls.model_fields.items()
        }
        cfg.update(model_fields)

        config_name = (
            config_name or getattr(cls._config_name_, "default")
        ) or cls._config_name_
        filename = f"{config_name}.yaml"
        config_root = config_root or global_hyfi.config_root
        config_path = config_path or getattr(cls._config_group_, "default") or "model"
        config_path = Path(config_root) / config_path
        config_path.mkdir(parents=True, exist_ok=True)
        config_path /= filename

        Composer.save(cfg, config_path)
        logger.info(f"Saved HyFI config for {cls.__name__} to {config_path}")
        return cfg


class TestModel(BaseModel):
    _config_name_: str = "__test__"
    _config_group_: str = "test"

    name: str = "test"

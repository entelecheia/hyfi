"""
    HiFY Base Model Class
"""
from pathlib import Path
from typing import Any, Dict, Optional, Set

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, model_validator

from hyfi.core import global_hyfi
from hyfi.utils.logging import LOGGING

from .composer import Composer
from .generator import sanitized_default_value

logger = LOGGING.getLogger(__name__)


class BaseModel(PydanticBaseModel):
    """
    Base class for all Pydantic models.

    Attributes:
        _config_name_ (str): The name of the model.
        _config_group_ (str): The group of the model.
        _auto_populate_ (bool): Whether to auto-populate the model with defaults from the config.
        _auto_generate_ (bool): Whether to auto-generate the config for the model.

    """

    _config_name_: str = "__init__"
    _config_group_: str = "/composer"
    _auto_populate_: bool = False
    _auto_generate_: bool = False
    _exclude_: Set[str] = set()
    _exclude_keys_ = {
        "_exclude_keys_": True,
        "_target_": True,
        "_config_name_": True,
        "_config_group_": True,
        "_auto_populate_": True,
        "_auto_generate_": True,
        "_exclude_": True,
    }

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=False,
    )  # type: ignore

    @model_validator(mode="before")
    def validate_model_config_before(cls, data):
        # logger.debug("Validating model config before validating each field.")
        _auto_populate_ = data.get("_auto_populate_", getattr(cls._auto_populate_, "default", False))  # type: ignore
        if not _auto_populate_:
            if global_hyfi.verbosity > 1:
                logger.debug("Auto-populate is disabled for class `%s`.", cls.__name__)
            return data
        _config_name_ = data.get("_config_name_", getattr(cls._config_name_, "default", "__init__"))  # type: ignore
        _config_group_ = data.get("_config_group_", getattr(cls._config_group_, "default"))  # type: ignore
        _class_name_ = cls.__name__  # type: ignore
        if not _config_group_:
            if global_hyfi.verbosity > 0:
                logger.debug("There is no config group specified.")
            return data
        # Initialize the config with the given config_name.
        if global_hyfi.verbosity > 1:
            logger.info(
                "Composing `%s` class with `%s` config in `%s` group.",
                _class_name_,
                _config_name_,
                _config_group_,
            )
        config_group = f"{_config_group_}={_config_name_}"
        cfg = Composer.compose_as_dict(
            config_group=config_group,
            config_data=data,
            throw_on_compose_failure=False,
        )
        data = Composer.update(cfg, data)
        # Exclude any attributes specified in the class's `exclude` list.
        exclude = getattr(cls._exclude_, "default", set())  # type: ignore
        for name in exclude:
            if name in data:
                logger.debug("Excluding `%s` from the config.", name)
                del data[name]  # type: ignore
        return data

    @property
    def kwargs(self) -> Dict[str, Any]:
        """
        Returns the model as a dictionary excluding any keys specified in the class's `exclude_keys` list.
        """
        return self.model_dump(exclude=self._exclude_keys_)

    @property
    def config_name(self) -> str:
        """
        Returns the name of the model.
        """
        return self._config_name_

    @property
    def config_group(self) -> str:
        """
        Returns the group of the model.
        """
        return self._config_group_

    @property
    def auto_populate(self) -> bool:
        """
        Returns whether the model should be auto-populated.
        """
        return self._auto_populate_

    @property
    def auto_generate(self) -> bool:
        """
        Returns whether the model should be auto-generated.
        """
        return self._auto_generate_

    @classmethod
    def generate_config(
        cls,
        config_name: Optional[str] = None,
        config_path: str = None,
        config_root: Optional[str] = None,
        save: bool = True,
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
        cfg = cls.sanitized_config(cfg)

        if not save:
            return cfg

        config_name = (
            config_name or getattr(cls._config_name_, "default")
        ) or cls._config_name_
        _save_config(
            config=cfg,
            class_name=cls.__name__,
            config_group=getattr(cls._config_group_, "default"),
            config_name=config_name,
            config_path=config_path,
            config_root=config_root,
        )
        return cfg

    @staticmethod
    def sanitized_config(
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Converts a config to Hydra-supported type if necessary and possible.

        Args:
            config (Dict[str, Any]): The config to sanitize.

        Returns:
            Dict[str, Any]: The sanitized config.
        """
        defaults = []
        sanitized_config = {}
        _config = {}
        for key, value in config.items():
            if hasattr(value, "_config_group_") and hasattr(value, "_config_name_"):
                config_name = (
                    getattr(value, "model_extra", {}).get("_config_name_")
                    or value._config_name_
                )
                if value._config_group_ == key:
                    defaults.append({f"{value._config_group_}": config_name})
                else:
                    defaults.append({f"{value._config_group_}@{key}": config_name})
            else:
                value = sanitized_default_value(value)
                _config[key] = value
        if defaults:
            sanitized_config["defaults"] = defaults
        sanitized_config.update(_config)
        return sanitized_config


def _save_config(
    config: Dict[str, Any],
    class_name: str,
    config_name: str,
    config_group: Optional[str] = None,
    config_root: Optional[str] = None,
    config_path: Optional[str] = None,
):
    filename = f"{config_name}.yaml"
    config_root = config_root or global_hyfi.config_root
    if config_group and config_group.startswith("/"):
        config_group = config_group[1:]
    config_path = config_path or config_group or "test"
    config_path = Path(config_root) / config_path
    config_path.mkdir(parents=True, exist_ok=True)
    config_path /= filename
    Composer.save(config, config_path)
    logger.info("Saved HyFI config for %s to %s", class_name, config_path)


class InnerTestModel(BaseModel):
    _config_name_: str = "__inner__"
    _config_group_: str = "/test"

    name: str = "inner"


class TestModel(BaseModel):
    _config_name_: str = "__test__"
    _config_group_: str = "/test"
    inner: InnerTestModel = InnerTestModel()

    name: str = "test"


__all__ = ["BaseModel", "model_validator"]

"""
    Hydra configuration management
"""
import functools
import json
import os
from enum import Enum
from pathlib import Path
from typing import IO, Any, Dict, List, Tuple, Union

import hydra
from omegaconf import DictConfig, ListConfig, OmegaConf, SCMode
from pydantic import BaseModel

from hyfi.__global__ import (
    __about__,
    __hydra_config__,
    __hydra_default_config_group_value__,
    __hydra_version_base__,
)
from hyfi.utils.logging import Logging

if level := os.environ.get("HYFI_LOG_LEVEL"):
    Logging.setLogger(level)
logger = Logging.getLogger(__name__)

DictKeyType = Union[str, int, Enum, float, bool]


class SpecialKeys(str, Enum):
    """Special keys in configs used by hyfi."""

    CALL = "_call_"
    CONFIG = "_config_"
    CONFIG_GROUP = "_config_group_"
    EXEC = "_exec_"
    FUNC = "_func_"
    METHOD = "_method_"
    NAME = "_name_"
    PARTIAL = "_partial_"
    rcPARAMS = "rcParams"
    RECURSIVE = "_recursive_"
    SUFFIX = "suffix"
    TARGET = "_target_"
    TYPE = "_type_"
    VERBOSE = "verbose"


class Composer(BaseModel):
    """
    Compose a configuration by applying overrides
    """

    config_group: Union[str, None] = None
    overrides: Union[List[str], None] = None
    config_data: Union[Dict[str, Any], DictConfig, None] = None
    throw_on_resolution_failure: bool = True
    throw_on_missing: bool = False
    config_name: Union[str, None] = None
    config_module: Union[str, None] = None
    global_package: bool = False
    verbose: bool = False

    __cfg__: DictConfig = None  # type: ignore

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
        underscore_attrs_are_private = True

    def __init__(self, **args):
        super().__init__(**args)
        self.__cfg__ = self.compose(
            config_group=self.config_group,
            overrides=self.overrides,
            config_data=self.config_data,
            throw_on_resolution_failure=self.throw_on_resolution_failure,
            throw_on_missing=self.throw_on_missing,
            root_config_name=self.config_name,
            config_module=self.config_module,
            global_package=self.global_package,
            verbose=self.verbose,
        )

    def compose(
        self,
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        global_package: bool = False,
        verbose: bool = False,
    ) -> DictConfig:
        """
        Compose a configuration by applying overrides

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group.key=value`)
            return_as_dict: Return the result as a dict
            throw_on_resolution_failure: If True throw an exception if resolution fails
            throw_on_missing: If True throw an exception if config_group doesn't exist
            root_config_name: Name of the root config to be used (e.g. `hconf`)
            config_module: Module of the config to be used (e.g. `hyfi.conf`)
            global_package: If True, the config assumed to be a global package
            verbose: If True print configuration to stdout

        Returns:
            A config object or a dictionary with the composed config
        """
        self.__cfg__ = Composer._compose(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            root_config_name=root_config_name,
            config_module=config_module,
            global_package=global_package,
            verbose=verbose,
        )
        return self.__cfg__

    @property
    def config(self) -> DictConfig:
        return self.__cfg__

    @property
    def config_as_dict(self) -> Dict:
        return Composer.to_dict(self.__cfg__)

    def __call__(
        self,
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        global_package: bool = False,
        verbose: bool = False,
    ) -> DictConfig:
        return self.compose(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            root_config_name=root_config_name,
            config_module=config_module,
            global_package=global_package,
            verbose=verbose,
        )

    def __getitem__(self, key):
        return self.__cfg__[key]

    def __getattr__(self, key):
        return getattr(self.__cfg__, key)

    def __repr__(self):
        return repr(self.__cfg__)

    def __str__(self):
        return str(self.__cfg__)

    def __iter__(self):
        return iter(self.__cfg__)

    def __len__(self):
        return len(self.__cfg__)

    def __contains__(self, key):
        return key in self.__cfg__

    def __eq__(self, other):
        return self.__cfg__ == other

    def __ne__(self, other):
        return self.__cfg__ != other

    def __bool__(self):
        return bool(self.__cfg__)

    def __hash__(self):
        return hash(self.__cfg__)

    def __getstate__(self):
        return self.__cfg__

    @staticmethod
    def select(
        cfg: Any,
        key: str,
        default: Any = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
    ):
        """
        Wrapper for OmegaConf. select value from a config object using a key.

        Args:
            cfg: Config node to select from
            key: Key to select
            default: Default value to return if key is not found
            throw_on_resolution_failure: Raise an exception if an interpolation
                resolution error occurs, otherwise return None
            throw_on_missing: Raise an exception if an attempt to select a missing key (with the value '???')
                is made, otherwise return None

        Returns:
            selected value or None if not found.
        """
        key = key.replace("/", ".")
        return OmegaConf.select(
            cfg,
            key=key,
            default=default,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
        )

    @staticmethod
    def to_dict(cfg: Any) -> Any:
        """
        Convert a config to a dict

        Args:
            cfg: The config to convert.

        Returns:
            The dict representation of the config.
        """
        # Convert a config object to a config object.
        if isinstance(cfg, dict):
            cfg = Composer.to_config(cfg)
        # Returns a container for the given config.
        if isinstance(cfg, (DictConfig, ListConfig)):
            return OmegaConf.to_container(
                cfg,
                resolve=True,
                throw_on_missing=False,
                structured_config_mode=SCMode.DICT,
            )
        return cfg

    @staticmethod
    def to_config(cfg: Any) -> Union[DictConfig, ListConfig]:
        """
        Convert a config object to OmegaConf

        Args:
            cfg: The config to convert.

        Returns:
            A Config object that corresponds to the given config.
        """
        return OmegaConf.create(cfg)

    @staticmethod
    def hydra_compose(
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
    ):
        is_initialized = hydra.core.global_hydra.GlobalHydra.instance().is_initialized()  # type: ignore
        config_module = config_module or __hydra_config__.hyfi_config_module
        logger.debug("config_module: %s", config_module)
        if is_initialized:
            # Hydra is already initialized.
            logger.debug("Hydra is already initialized")
            cfg = hydra.compose(config_name=root_config_name, overrides=overrides)
        else:
            with hydra.initialize_config_module(
                config_module=config_module, version_base=__hydra_version_base__
            ):
                cfg = hydra.compose(config_name=root_config_name, overrides=overrides)
        if is_initialized:
            cfg = hydra.compose(config_name=root_config_name, overrides=overrides)
        else:
            with hydra.initialize_config_module(
                config_module=config_module, version_base=__hydra_version_base__
            ):
                cfg = hydra.compose(config_name=root_config_name, overrides=overrides)
        return cfg

    @staticmethod
    def split_config_group(
        config_group: Union[str, None] = None,
    ) -> Tuple[str, str, str]:
        if config_group:
            group_ = config_group.split("=")
            # group_key group_value group_key group_value group_key group_value default
            if len(group_) == 2:
                group_key, group_value = group_
            else:
                group_key = group_[0]
                group_value = __hydra_default_config_group_value__
            config_group = f"{group_key}={group_value}"
        else:
            group_key = ""
            group_value = ""
            config_group = ""
        return config_group, group_key, group_value

    @staticmethod
    def _compose(
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        global_package: bool = False,
        **kwargs,
    ) -> DictConfig:
        if isinstance(config_data, DictConfig):
            logger.debug("returning config_group_kwargs without composing")
            return config_data
        # Set overrides to the empty list if None
        if overrides is None:
            overrides = []
        # Set the group key and value of the config group.
        config_group, group_key, group_value = Composer.split_config_group(config_group)
        # If group_key and group_value are specified in the configuration file.
        if group_key and group_value:
            # Initialize hydra configuration module.
            cfg = Composer.hydra_compose(
                root_config_name=root_config_name,
                config_module=config_module,
                overrides=overrides,
            )
            cfg = Composer.select(
                cfg,
                key=group_key,
                default=None,
                throw_on_missing=False,
                throw_on_resolution_failure=False,
            )
            override = config_group if cfg is not None else f"+{config_group}"
            # Add override to overrides list.
            if isinstance(override, str):
                if overrides:
                    overrides.append(override)
                else:
                    overrides = [override]
        # if verbose:
        logger.debug(f"compose config with overrides: {overrides}")
        # Initialize hydra and return the configuration.
        cfg = Composer.hydra_compose(
            root_config_name=root_config_name,
            config_module=config_module,
            overrides=overrides,
        )
        # Add config group overrides to overrides list.
        group_overrides = []
        group_cfg = Composer.select(
            cfg,
            key=group_key,
            default=None,
            throw_on_missing=False,
            throw_on_resolution_failure=False,
        )
        if config_data and group_cfg:
            group_overrides.extend(
                f"{group_key}.{k}={v}"
                for k, v in config_data.items()
                if isinstance(v, (str, int, float, bool)) and k in group_cfg
            )
        if group_overrides:
            overrides.extend(group_overrides)
            cfg = Composer.hydra_compose(
                root_config_name=root_config_name,
                config_module=config_module,
                overrides=overrides,
            )

        # Select the group_key from the configuration.
        if group_key and not global_package:
            cfg = Composer.select(
                cfg,
                key=group_key,
                default=None,
                throw_on_missing=throw_on_missing,
                throw_on_resolution_failure=throw_on_resolution_failure,
            )
        # logger.debug("Composed config: %s", OmegaConf.to_yaml(_to_dict(cfg)))
        return cfg

    @staticmethod
    def print(cfg: Any, resolve: bool = True, **kwargs):
        import pprint

        if Composer.is_config(cfg):
            if resolve:
                pprint.pprint(Composer.to_dict(cfg), **kwargs)
            else:
                pprint.pprint(cfg, **kwargs)
        else:
            print(cfg)

    @staticmethod
    def is_config(
        cfg: Any,
    ):
        return isinstance(cfg, (DictConfig, dict))

    @staticmethod
    def is_list(
        cfg: Any,
    ):
        return isinstance(cfg, (ListConfig, list))

    @staticmethod
    def is_instantiatable(cfg: Any):
        return Composer.is_config(cfg) and SpecialKeys.TARGET in cfg

    @staticmethod
    def load(file_: Union[str, Path, IO[Any]]) -> Union[DictConfig, ListConfig]:
        return OmegaConf.load(file_)

    @staticmethod
    def save(config: Any, f: Union[str, Path, IO[Any]], resolve: bool = False) -> None:
        os.makedirs(os.path.dirname(str(f)), exist_ok=True)
        OmegaConf.save(config, f, resolve=resolve)

    @staticmethod
    def save_json(
        json_dict: dict,
        f: Union[str, Path, IO[Any]],
        indent=4,
        ensure_ascii=False,
        default=None,
        encoding="utf-8",
        **kwargs,
    ):
        f = str(f)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding=encoding) as f:
            json.dump(
                json_dict,
                f,
                indent=indent,
                ensure_ascii=ensure_ascii,
                default=default,
                **kwargs,
            )

    @staticmethod
    def load_json(f: Union[str, Path, IO[Any]], encoding="utf-8", **kwargs) -> dict:
        f = str(f)
        with open(f, "r", encoding=encoding) as f:
            return json.load(f, **kwargs)

    @staticmethod
    def update(_dict, _overrides):
        import collections.abc

        for k, v in _overrides.items():
            if isinstance(v, collections.abc.Mapping):
                _dict[k] = Composer.update((_dict.get(k) or {}), v)
            else:
                _dict[k] = v
        return _dict

    @staticmethod
    def merge(
        *configs: Union[
            DictConfig,
            ListConfig,
            Dict[DictKeyType, Any],
            List[Any],
            Tuple[Any, ...],
            Any,
        ],
    ) -> Union[ListConfig, DictConfig]:
        """
        Merge a list of previously created configs into a single one
        :param configs: Input configs
        :return: the merged config object.
        """
        return OmegaConf.merge(*configs)

    @staticmethod
    def to_yaml(cfg: Any, resolve: bool = False, sort_keys: bool = False) -> str:
        if resolve:
            cfg = Composer.to_dict(cfg)
        return OmegaConf.to_yaml(cfg, resolve=resolve, sort_keys=sort_keys)

    @staticmethod
    def to_container(
        cfg: Any,
        resolve: bool = False,
        throw_on_missing: bool = False,
        enum_to_str: bool = False,
        structured_config_mode: SCMode = SCMode.DICT,
    ):
        return OmegaConf.to_container(
            cfg,
            resolve=resolve,
            throw_on_missing=throw_on_missing,
            enum_to_str=enum_to_str,
            structured_config_mode=structured_config_mode,
        )

    @staticmethod
    def methods(cfg: Any, obj: object, return_function=False):
        cfg = Composer.to_dict(cfg)
        if not cfg:
            logger.info("No method defined to call")
            return

        if isinstance(cfg, dict) and SpecialKeys.METHOD in cfg:
            _method_ = cfg[SpecialKeys.METHOD]
        elif isinstance(cfg, dict):
            _method_ = cfg
        elif isinstance(cfg, str):
            _method_ = cfg
            cfg = {}
        else:
            raise ValueError(f"Invalid method: {cfg}")

        if isinstance(_method_, str):
            _fn = getattr(obj, _method_)
            if return_function:
                logger.info(f"Returning function {_fn}")
                return _fn
            logger.info(f"Calling {_method_}")
            return _fn(**cfg)
        elif isinstance(_method_, dict):
            if SpecialKeys.CALL in _method_:
                _call_ = _method_.pop(SpecialKeys.CALL)
            else:
                _call_ = True
            if _call_:
                _fn = getattr(obj, _method_[SpecialKeys.METHOD_NAME])
                _parms = _method_.pop(SpecialKeys.rcPARAMS, {})
                if return_function:
                    if not _parms:
                        logger.info(f"Returning function {_fn}")
                        return _fn
                    logger.info(f"Returning function {_fn} with params {_parms}")
                    return functools.partial(_fn, **_parms)
                logger.info(f"Calling {_method_}")
                return _fn(**_parms)
            else:
                logger.info(f"Skipping call to {_method_}")
        elif isinstance(_method_, list):
            for _each_method in _method_:
                logger.info(f"Calling {_each_method}")
                if isinstance(_each_method, str):
                    getattr(obj, _each_method)()
                elif isinstance(_each_method, dict):
                    if SpecialKeys.CALL in _each_method:
                        _call_ = _each_method.pop(SpecialKeys.CALL)
                    else:
                        _call_ = True
                    if _call_:
                        getattr(obj, _each_method[SpecialKeys.METHOD_NAME])(
                            **_each_method[SpecialKeys.rcPARAMS]
                        )
                    else:
                        logger.info(f"Skipping call to {_each_method}")

    @staticmethod
    def ensure_list(value):
        if not value:
            return []
        elif isinstance(value, str):
            return [value]
        return Composer.to_dict(value)

    @staticmethod
    def ensure_kwargs(_kwargs, _fn):
        from inspect import getfullargspec as getargspec

        if callable(_fn):
            args = getargspec(_fn).args
            logger.info(f"args of {_fn}: {args}")
            return {k: v for k, v in _kwargs.items() if k in args}
        return _kwargs


class BaseConfig(BaseModel):
    config_name: str = "__init__"
    config_group: str = ""

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
        validate_assignment = True
        exclude = {}
        include = {}
        underscore_attrs_are_private = True
        property_set_methods = {}

    def __init__(self, **config_kwargs):
        super().__init__(**config_kwargs)
        self.initialize_configs(**config_kwargs)

    def __setattr__(self, key, val):
        super().__setattr__(key, val)
        if method := self.__config__.property_set_methods.get(key):  # type: ignore
            getattr(self, method)(val)

    def initialize_configs(
        self,
        **config_kwargs,
    ):
        if not self.config_group:
            logger.debug("There is no config group specified.")
            return
        # Initialize the config with the given config_name.
        logger.debug(
            "Initializing `%s` class with `%s` config in `%s` group.",
            self.__class__.__name__,
            self.config_name,
            self.config_group,
        )
        config_kwargs = Composer(
            config_group=f"{self.config_group}={self.config_name}",
            config_data=config_kwargs,
        ).config_as_dict
        self.__dict__.update(config_kwargs)

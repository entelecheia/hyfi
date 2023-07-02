"""
    Hydra configuration management
"""
import collections.abc
import json
import os
import re
from enum import Enum
from pathlib import Path
from typing import IO, Any, Dict, List, Mapping, Optional, Set, Tuple, Union

import hydra
from omegaconf import DictConfig, ListConfig, OmegaConf, SCMode
from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator

from hyfi.__global__ import (
    __about__,
    __hydra_config__,
    __hydra_default_config_group_value__,
    __hydra_version_base__,
)
from hyfi.utils.logging import LOGGING

if level := os.environ.get("HYFI_LOG_LEVEL"):
    LOGGING.setLogger(level)
logger = LOGGING.getLogger(__name__)

DictKeyType = Union[str, int, Enum, float, bool]


class SpecialKeys(str, Enum):
    """Special keys in configs used by HyFI."""

    CALL = "_call_"
    CONFIG = "_config_"
    CONFIG_GROUP = "_config_group_"
    CONFIG_NAME = "_config_name_"
    EXEC = "_exec_"
    FUNC = "_func_"
    KWARGS = "_kwargs_"
    METHOD = "_method_"
    PARTIAL = "_partial_"
    PIPE = "_pipe_"
    RECURSIVE = "_recursive_"
    RUN = "_run_"
    TARGET = "_target_"
    TYPE = "_type_"
    WITH = "_with_"


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

    _cfg_: DictConfig = PrivateAttr({})

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )  # type: ignore

    def __init__(self, **args):
        super().__init__(**args)
        self._cfg_ = self.compose(
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
        self._cfg_ = Composer._compose(
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
        return self._cfg_

    @property
    def config(self) -> DictConfig:
        """
        Returns the composed configuration.
        """
        return self._cfg_

    @property
    def config_as_dict(self) -> Dict:
        """
        Return the configuration as a dictionary.
        """
        return Composer.to_dict(self._cfg_)

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
        return self._cfg_[key]

    def __iter__(self):
        return iter(self._cfg_)

    def __len__(self):
        return len(self._cfg_)

    def __contains__(self, key):
        return key in self._cfg_

    def __eq__(self, other):
        return self._cfg_ == other

    def __ne__(self, other):
        return self._cfg_ != other

    def __bool__(self):
        return bool(self._cfg_)

    def __hash__(self):
        return hash(self._cfg_)

    def __getstate__(self):
        return self._cfg_

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
    def _compose_as_dict(
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        global_package: bool = False,
        **kwargs,
    ) -> Dict:
        return Composer.to_dict(
            Composer._compose(
                config_group=config_group,
                overrides=overrides,
                config_data=config_data,
                throw_on_resolution_failure=throw_on_resolution_failure,
                throw_on_missing=throw_on_missing,
                root_config_name=root_config_name,
                config_module=config_module,
                global_package=global_package,
                **kwargs,
            )
        )

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
        group_overrides: List[str] = []
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
        """
        Prints the configuration object in a human-readable format.

        Args:
            cfg (Any): The configuration object to print.
            resolve (bool, optional): Whether to resolve the configuration object before printing. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the pprint.pprint function.

        Returns:
            None
        """
        import pprint

        if Composer.is_config(cfg):
            if resolve:
                pprint.pprint(Composer.to_dict(cfg), **kwargs)
            else:
                pprint.pprint(cfg, **kwargs)
        else:
            print(cfg)

    @staticmethod
    def is_config(cfg: Any):
        """
        Determines whether the input object is a valid configuration object.

        Args:
            cfg (Any): The object to check.

        Returns:
            bool: True if the object is a valid configuration object, False otherwise.
        """
        return isinstance(cfg, (DictConfig, dict))

    @staticmethod
    def is_list(cfg: Any):
        """
        Determines whether the input object is a valid list configuration object.

        Args:
            cfg (Any): The object to check.

        Returns:
            bool: True if the object is a valid list configuration object, False otherwise.
        """
        return isinstance(cfg, (ListConfig, list))

    @staticmethod
    def is_instantiatable(cfg: Any):
        """
        Determines whether the input configuration object is instantiatable.

        Args:
            cfg (Any): The configuration object to check.

        Returns:
            bool: True if the configuration object is instantiatable, False otherwise.
        """
        return Composer.is_config(cfg) and SpecialKeys.TARGET in cfg

    @staticmethod
    def load(file_: Union[str, Path, IO[Any]]) -> Union[DictConfig, ListConfig]:
        """
        Load a configuration file and return a configuration object.

        Args:
            file_ (Union[str, Path, IO[Any]]): The path to the configuration file or a file-like object.

        Returns:
            Union[DictConfig, ListConfig]: The configuration object.
        """
        return OmegaConf.load(file_)

    @staticmethod
    def save(config: Any, f: Union[str, Path, IO[Any]], resolve: bool = False) -> None:
        """
        Save a configuration object to a file.

        Args:
            config (Any): The configuration object to save.
            f (Union[str, Path, IO[Any]]): The path to the file or a file-like object.
            resolve (bool, optional): Whether to resolve the configuration object before saving. Defaults to False.
        """
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
        """
        Save a dictionary to a JSON file.

        Args:
            json_dict (dict): The dictionary to save.
            f (Union[str, Path, IO[Any]]): The path to the file or a file-like object.
            indent (int, optional): The number of spaces to use for indentation. Defaults to 4.
            ensure_ascii (bool, optional): Whether to escape non-ASCII characters. Defaults to False.
            default (Any, optional): A function to convert non-serializable objects. Defaults to None.
            encoding (str, optional): The encoding to use. Defaults to "utf-8".
            **kwargs: Additional arguments to pass to json.dump().
        """
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
        """
        Load a JSON file into a dictionary.

        Args:
            f (Union[str, Path, IO[Any]]): The path to the file or a file-like object.
            encoding (str, optional): The encoding to use. Defaults to "utf-8".
            **kwargs: Additional arguments to pass to json.load().

        Returns:
            dict: The dictionary loaded from the JSON file.
        """
        f = str(f)
        with open(f, "r", encoding=encoding) as f:
            return json.load(f, **kwargs)

    @staticmethod
    def update(_dict: Mapping[str, Any], _overrides: Mapping[str, Any]) -> Mapping:
        """
        Update a dictionary with overrides.

        Args:
            _dict (Mapping[str, Any]): The dictionary to update.
            _overrides (Mapping[str, Any]): The dictionary with overrides.

        Returns:
            Mapping: The updated dictionary.
        """
        for k, v in _overrides.items():
            if isinstance(v, collections.abc.Mapping):
                _dict[k] = Composer.update((_dict.get(k) or {}), v)  # type: ignore
            else:
                _dict[k] = v  # type: ignore
        return _dict

    @staticmethod
    def replace_keys(_dict: Mapping[str, Any], old_key: str, new_key: str) -> Mapping:
        """
        Replace a key in a dictionary.

        Args:
            _dict (Mapping[str, Any]): The dictionary to update.
            old_key (str): The old key to replace.
            new_key (str): The new key to use.

        Returns:
            Mapping: The updated dictionary.
        """
        _new_dict = {}
        for k, v in _dict.items():
            key = new_key if k == old_key else k
            if isinstance(v, collections.abc.Mapping):
                _new_dict[key] = Composer.replace_keys(v, old_key, new_key)
            else:
                _new_dict[key] = v
        return _new_dict

    @staticmethod
    def replace_special_keys(_dict: Mapping[str, Any]) -> Mapping:
        """
        Replace special keys in a dictionary.

        Args:
            _dict (Mapping[str, Any]): The dictionary to update.

        Returns:
            Mapping: The updated dictionary.
        """
        _new_dict = {}
        for k, v in _dict.items():
            key = Composer.generate_alias_for_special_keys(k)
            if isinstance(v, collections.abc.Mapping):
                _new_dict[key] = Composer.replace_special_keys(v)
            else:
                _new_dict[key] = v
        return _new_dict

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
        Merge a list of previously created configs into a single one.

        Args:
            *configs: Input configs.

        Returns:
            Union[ListConfig, DictConfig]: The merged config object.
        """
        return OmegaConf.merge(*configs)

    @staticmethod
    def merge_as_dict(
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
        Merge a list of previously created configs into a single dictionary.

        Args:
            *configs: Input configs.

        Returns:
            Union[ListConfig, DictConfig]: The merged config object as a dictionary.
        """
        return Composer.to_dict(OmegaConf.merge(*configs))

    @staticmethod
    def to_yaml(cfg: Any, resolve: bool = False, sort_keys: bool = False) -> str:
        """
        Convert the input config object to a YAML string.

        Args:
            cfg (Any): The input config object.
            resolve (bool, optional): Whether to resolve the config object before converting it to YAML. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the resulting YAML string. Defaults to False.

        Returns:
            str: The YAML string representation of the input config object.
        """
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
        """
        Convert the input config object to a nested container (e.g. dictionary).

        Args:
            cfg (Any): The input config object.
            resolve (bool, optional): Whether to resolve the config object before converting it to a container. Defaults to False.
            throw_on_missing (bool, optional): Whether to throw an exception if a missing key is encountered. Defaults to False.
            enum_to_str (bool, optional): Whether to convert enum values to strings. Defaults to False.
            structured_config_mode (SCMode, optional): The structured config mode to use. Defaults to SCMode.DICT.

        Returns:
            The nested container (e.g. dictionary) representation of the input config object.
        """
        return OmegaConf.to_container(
            cfg,
            resolve=resolve,
            throw_on_missing=throw_on_missing,
            enum_to_str=enum_to_str,
            structured_config_mode=structured_config_mode,
        )

    @staticmethod
    def ensure_list(value):
        """
        Ensure that the given value is a list. If the value is None or an empty string, an empty list is returned.
        If the value is already a list, it is returned as is. If the value is a string, it is returned as a list
        containing only that string. Otherwise, the value is converted to a dictionary using the Composer.to_dict method
        and the resulting dictionary is returned as a list.

        Args:
            value (Any): The value to ensure as a list.

        Returns:
            List: The value as a list.
        """
        if not value:
            return []
        elif isinstance(value, str):
            return [value]
        return Composer.to_dict(value)

    @staticmethod
    def ensure_kwargs(_kwargs, _fn):
        """
        Ensure that the given keyword arguments are valid for the given function.

        Args:
            _kwargs (dict): The keyword arguments to validate.
            _fn (callable): The function to validate the keyword arguments against.

        Returns:
            dict: The valid keyword arguments for the given function.
        """
        from inspect import getfullargspec as getargspec

        if callable(_fn):
            args = getargspec(_fn).args
            logger.info(f"args of {_fn}: {args}")
            return {k: v for k, v in _kwargs.items() if k in args}
        return _kwargs

    @staticmethod
    def generate_alias_for_special_keys(key: str) -> str:
        """
        Generate an alias for special keys.
        _with_ -> run_with
        _pipe_ -> run_pipe
        _run_ -> run

        Args:
            key (str): The special key to generate an alias for.

        Returns:
            str: The alias for the special key.
        """
        # replace the exact `with`, `pipe` with `run_with`, `run_pipe`
        key_ = re.sub(r"^with$", "run_with", key)
        # replace the prefix `_` with `run_`
        key_ = re.sub(r"^_with_$", "run_with", key_)
        key_ = re.sub(r"^_pipe_$", "pipe_target", key_)
        key_ = re.sub(r"^_run_$", "run", key_)
        return key_


class BaseConfig(BaseModel):
    """
    Base class for all config classes.
    """

    _config_name_: str = "__init__"
    _config_group_: str = ""
    verbose: bool = False

    _init_args_: Dict[str, Any] = {}
    _exclude_: Set[str] = set()
    _property_set_methods_: Dict[str, str] = {}

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=False,
    )  # type: ignore

    def __init__(self, **config_kwargs):
        logger.debug("init %s with %s", self.__class__.__name__, config_kwargs)
        super().__init__(**config_kwargs)

    def __setattr__(self, key, val):
        """
        Overrides the default __setattr__ method to allow for custom property set methods.

        Args:
            key (str): The name of the attribute to set.
            val (Any): The value to set the attribute to.
        """
        if method := self._property_set_methods_.get(key):  # type: ignore
            logger.info(
                "Setting %s to %s",
                key,
                val if isinstance(val, (str, int)) else type(val),
            )
            getattr(self, method)(val)
        super().__setattr__(key, val)

    @model_validator(mode="before")
    def validate_model_config_before(cls, data):
        logger.debug("validate_model_config_before: %s", data)
        _config_name_ = data.get("_config_name_", getattr(cls._config_name_, "default", "__init__"))  # type: ignore
        _config_group_ = data.get("_config_group_", getattr(cls._config_group_, "default"))  # type: ignore
        _class_name_ = cls.__name__  # type: ignore
        if not _config_group_:
            logger.debug("There is no config group specified.")
            return data
        # Initialize the config with the given config_name.
        logger.info(
            "Composing `%s` class with `%s` config in `%s` group.",
            _class_name_,
            _config_name_,
            _config_group_,
        )
        data = Composer(
            config_group=f"{_config_group_}={_config_name_}",
            config_data=data,
        ).config_as_dict
        return data

    # @model_validator(mode="after")  # type: ignore
    # def validate_model_config_after(cls, model):
    #     logger.debug("validate_model_config_after")
    #     return model

    def export_config(
        self,
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> Dict[str, Any]:
        """
        Export the configuration to a dictionary.

        Args:
            exclude (Optional[Union[str, List[str], Set[str], None]]): Keys to exclude from the saved configuration.
                Defaults to None.
            exclude_none (bool): Whether to exclude keys with None values. Defaults to True.
            only_include (Optional[Union[str, List[str], Set[str], None]]): Keys to include in the saved configuration.
                Defaults to None.

        Returns:
            Dict[str, Any]: The configuration dictionary.
        """
        if not exclude:
            exclude = self._exclude_  # type: ignore
        if isinstance(exclude, str):
            exclude = [exclude]
        if exclude is None:
            exclude = []
        if isinstance(only_include, str):
            only_include = [only_include]
        if only_include is None:
            only_include = []

        config = self.model_dump(exclude=exclude, exclude_none=exclude_none)  # type: ignore
        if only_include:
            config = {key: config[key] for key in only_include if key in config}

        return config

    def save_config(
        self,
        filepath: Union[str, Path],
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> str:
        """
        Save the batch configuration to file.

        Args:
            filepath ([Union[str, Path]): The filepath to save the configuration to.
            exclude (Optional[Union[str, List[str], Set[str], None]]): Keys to exclude from the saved configuration.
                Defaults to None.
            exclude_none (bool): Whether to exclude keys with None values. Defaults to True.
            only_include (Optional[Union[str, List[str], Set[str], None]]): Keys to include in the saved configuration.
                Defaults to None.

        Returns:
            str: The filename of the saved configuration.
        """
        logger.info("Saving config to %s", filepath)

        config_to_save = self.export_config(
            exclude=exclude, exclude_none=exclude_none, only_include=only_include
        )

        Composer.save(config_to_save, filepath)
        return str(filepath)

    def save_config_as_json(
        self,
        filepath: Union[str, Path],
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> str:
        def dumper(obj):
            return Composer.to_dict(obj) if isinstance(obj, DictConfig) else str(obj)

        config_to_save = self.export_config(
            exclude=exclude, exclude_none=exclude_none, only_include=only_include
        )
        logger.info("Saving config to %s", filepath)
        Composer.save_json(config_to_save, filepath, default=dumper)
        return str(filepath)

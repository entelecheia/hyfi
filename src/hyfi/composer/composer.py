"""
    Hydra configuration management
"""
import collections.abc
import os
import re
from enum import Enum
from typing import Any, Callable, Dict, List, Mapping, Optional, Union

import hydra
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig
from pydantic import BaseModel

from hyfi.core import global_hyfi
from hyfi.core import hydra as hyfi_hydra
from hyfi.utils import UTILs

from .generator import GENERATOR

if level := os.environ.get("HYFI_LOG_LEVEL"):
    UTILs.setLogger(level)
logger = UTILs.getLogger(__name__)


class SpecialKeys(str, Enum):
    """Special keys in configs used by HyFI."""

    CALL = "_call_"
    CONFIG = "_config_"
    CONFIG_GROUP = "_config_group_"
    CONFIG_NAME = "_config_name_"
    DESCRIPTION = "_description_"
    EXEC = "_exec_"
    FUNC = "_func_"
    KWARGS = "_kwargs_"
    METHOD = "_method_"
    PARTIAL = "_partial_"
    PIPE_TARGET = "pipe_target"
    RECURSIVE = "_recursive_"
    RUN = "run"
    RUN_WITH = "run_with"
    TARGET = "_target_"
    TYPE = "_type_"
    USES = "uses"
    WITH = "with"


class ConfigGroup(BaseModel):
    config_group: str = ""
    _group_override_: str = ""
    _group_key_: str = ""
    _group_value_: str = ""
    _global_package_: bool = False

    @property
    def group_override(self):
        if not self._group_override_:
            self._split_config_group()
        return self._group_override_

    @property
    def group_key(self):
        if not self._group_key_:
            self._split_config_group()
        return self._group_key_

    @property
    def group_value(self):
        if not self._group_value_:
            self._split_config_group()
        return self._group_value_

    @property
    def global_package(self):
        return self._global_package_

    def get_overrides(
        self,
        overrides: Optional[List[str]] = None,
        root_config_name: Optional[str] = None,
        config_module: Optional[str] = None,
    ) -> List[str]:
        if overrides is None:
            overrides = []
        if self.group_key in global_hyfi.global_package_list:
            self._global_package_ = True
        # If group_key and group_value are specified in the configuration file.
        if self.group_key and self.group_value:
            config = Composer.hydra_compose(
                root_config_name=root_config_name,
                config_module=config_module,
            )
            config = Composer.select(
                config,
                key=self.group_key,
                default=None,
                throw_on_missing=False,
                throw_on_resolution_failure=False,
            )
            override = (
                self.group_override if config is not None else f"+{self.group_override}"
            )
            # Add override to overrides list.
            if override and override not in overrides:
                overrides = [override] + overrides

        return overrides

    def _split_config_group(self):
        config_group = self.config_group
        if config_group:
            group_ = config_group.split("=")
            # group_key group_value group_key group_value group_key group_value default
            if len(group_) == 2:
                group_key, group_value = group_
            else:
                group_key = group_[0]
                group_value = global_hyfi.hydra_default_config_group_value
            # remove leading slash
            if group_key.startswith("/"):
                group_key = group_key[1:]
            config_group = f"{group_key}={group_value}"
        else:
            group_key = ""
            group_value = ""
            config_group = ""
        self._group_override_ = config_group
        self._group_key_ = group_key
        self._group_value_ = group_value


class Composer(UTILs, GENERATOR):
    """
    Compose a configuration by applying overrides
    """

    @staticmethod
    def hydra_compose(
        root_config_name: Optional[str] = None,
        config_module: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        plugins: Optional[List[str]] = None,
    ):
        is_initialized = GlobalHydra.instance().is_initialized()  # type: ignore
        config_module = config_module or global_hyfi.config_module
        plugins = plugins or global_hyfi.plugins

        overrides = overrides or []
        # by adding the variables=__init__ override,
        # we can access the variables in the config whenever we want
        override = "+variables=__init__"
        if override not in overrides:
            overrides.append(override)
            logger.debug(
                "Overriding `about` config group with `%s`",
                global_hyfi.package_name,
            )
        # logger.debug("config_module: %s", config_module)
        if is_initialized:
            # Hydra is already initialized.
            # logger.debug("Hydra is already initialized")
            cfg = hydra.compose(config_name=root_config_name, overrides=overrides)
        else:
            with hyfi_hydra.initialize_config(
                config_module=config_module,
                config_dir=global_hyfi.user_config_path,
                plugins=plugins,
                version_base=global_hyfi.hydra_version_base,
            ):
                cfg = hydra.compose(config_name=root_config_name, overrides=overrides)
        return cfg

    @staticmethod
    def compose_as_dict(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        throw_on_compose_failure: bool = True,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Optional[str] = None,
        config_module: Optional[str] = None,
        global_package: bool = False,
        **kwargs,
    ) -> Dict:
        return Composer.to_dict(
            Composer.compose(
                config_group=config_group,
                overrides=overrides,
                config_data=config_data,
                throw_on_compose_failure=throw_on_compose_failure,
                throw_on_resolution_failure=throw_on_resolution_failure,
                throw_on_missing=throw_on_missing,
                root_config_name=root_config_name,
                config_module=config_module,
                global_package=global_package,
                **kwargs,
            )
        )

    @staticmethod
    def compose(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        throw_on_compose_failure: bool = True,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Optional[str] = None,
        config_module: Optional[str] = None,
        global_package: bool = False,
        **kwargs,
    ) -> DictConfig:
        try:
            return Composer._compose_internal(
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
        except Exception as e:
            logger.error("Error composing config: %s", e)
            if throw_on_compose_failure:
                raise e
            return DictConfig(config_data) if config_data else DictConfig({})

    @staticmethod
    def _compose_internal(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Optional[str] = None,
        config_module: Optional[str] = None,
        global_package: bool = False,
        **kwargs,
    ) -> DictConfig:
        if isinstance(config_data, DictConfig):
            logger.debug("returning config_data without composing")
            return config_data
        cg = ConfigGroup(config_group=config_group)
        overrides = cg.get_overrides(
            overrides=overrides,
            root_config_name=root_config_name,
            config_module=config_module,
        )

        logger.debug(f"compose config with overrides: {overrides}")
        # Initialize hydra and return the configuration.
        cfg = Composer.hydra_compose(
            root_config_name=root_config_name,
            config_module=config_module,
            overrides=overrides,
        )
        # Add config group overrides to overrides list.
        global_package = global_package or cg.global_package
        if cg.group_key and not global_package:
            group_overrides: List[str] = []
            group_cfg = Composer.select(
                cfg,
                key=cg.group_key,
                default=None,
                throw_on_missing=False,
                throw_on_resolution_failure=False,
            )
            if config_data and group_cfg:
                group_overrides.extend(
                    f"{cg.group_key}.{k}='{v}'"
                    if isinstance(v, str)
                    else f"{cg.group_key}.{k}={v}"
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
            cfg = Composer.select(
                cfg,
                key=cg.group_key,
                default=None,
                throw_on_missing=throw_on_missing,
                throw_on_resolution_failure=throw_on_resolution_failure,
            )
        return cfg

    @staticmethod
    def is_composable(
        config_group: str,
        config_module: Optional[str] = None,
    ) -> bool:
        """
        Determines whether the input configuration object is composable.

        Args:
            config_group (str): The name of the configuration group to check.
            config_module (Optional[str], optional): The name of the configuration module to check. Defaults to None.

        Returns:
            bool: True if the configuration object is composable, False otherwise.
        """
        try:
            cfg = Composer.compose(
                config_group=config_group,
                config_module=config_module,
            )
            return cfg is not None
        except Exception as e:
            logger.error("Error composing config: %s", e)
            return False

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
    def generate_alias_for_special_keys(key: str) -> str:
        """
        Generate an alias for special keys.
        _with_ -> run
        _pipe_ -> pipe_target
        _run_ -> run

        Args:
            key (str): The special key to generate an alias for.

        Returns:
            str: The alias for the special key.
        """
        # replace the exact `with`, `pipe` with `run_with`, `run_pipe`
        key_ = re.sub(r"^with$", "run", key)
        # replace the prefix `_` with `run_`
        key_ = re.sub(r"^_with_$", "run", key_)
        key_ = re.sub(r"^_pipe_$", "pipe_target", key_)
        key_ = re.sub(r"^_run_$", "run", key_)
        return key_

    @staticmethod
    def partial(
        config: Union[str, Dict],
        *args: Any,
        **kwargs: Any,
    ) -> Callable:
        """
        Returns a callable object that is a partial version of the function or class specified in the config object.

        Args:
            config: An config object describing what to call and what params to use.
                    In addition to the parameters, the config must contain:
                    _target_ : target class or callable name (str)
                    And may contain:
                    _partial_: If True, return functools.partial wrapped method or object
                                False by default. Configure per target.
            args: Optional positional parameters pass-through
            kwargs: Optional named parameters to override
                    parameters in the config object. Parameters not present
                    in the config objects are being passed as is to the target.
                    IMPORTANT: dataclasses instances in kwargs are interpreted as config
                                and cannot be used as passthrough
        Returns:
            A callable object that is a partial version of the function or class specified in the config object.
        """
        if isinstance(config, str):
            config = {SpecialKeys.TARGET.value: config}
        else:
            config = Composer.to_dict(config)
        if not isinstance(config, dict):
            raise ValueError("config must be a dict or a str")
        config[SpecialKeys.PARTIAL.value] = True
        rc_kwargs_ = config.pop(SpecialKeys.KWARGS, {})
        if rc_kwargs_ and kwargs:
            kwargs.update(rc_kwargs_)
        return Composer.instantiate(config, *args, **kwargs)

    @staticmethod
    def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Instantiates an object using the provided config object.

        Args:
            config: An config object describing what to call and what params to use.
                    In addition to the parameters, the config must contain:
                    _target_ : target class or callable name (str)
                    And may contain:
                    _args_: List-like of positional arguments to pass to the target
                    _recursive_: Construct nested objects as well (bool).
                                    False by default.
                                    may be overridden via a _recursive_ key in
                                    the kwargs
                    _convert_: Conversion strategy
                            none    : Passed objects are DictConfig and ListConfig, default
                            partial : Passed objects are converted to dict and list, with
                                    the exception of Structured Configs (and their fields).
                            all     : Passed objects are dicts, lists and primitives without
                                    a trace of OmegaConf containers
                    _partial_: If True, return functools.partial wrapped method or object
                                False by default. Configure per target.
                    _args_: List-like of positional arguments
            args: Optional positional parameters pass-through
            kwargs: Optional named parameters to override
                    parameters in the config object. Parameters not present
                    in the config objects are being passed as is to the target.
                    IMPORTANT: dataclasses instances in kwargs are interpreted as config
                                and cannot be used as passthrough

        Returns:
            if _target_ is a class name: the instantiated object
            if _target_ is a callable: the return value of the call
        """
        verbose = config.get("verbose", False)
        if not Composer.is_instantiatable(config):
            if verbose:
                logger.info("Config is not instantiatable, returning config")
            return config
        _recursive_ = config.get(SpecialKeys.RECURSIVE, False)
        if SpecialKeys.RECURSIVE not in kwargs:
            kwargs[SpecialKeys.RECURSIVE.value] = _recursive_
        if verbose:
            logger.info("instantiating %s ...", config.get(SpecialKeys.TARGET))
        return hydra.utils.instantiate(config, *args, **kwargs)

    @staticmethod
    def getsource(obj: Any) -> str:
        """
        Return the source code of the object.

        Args:
            obj: The object to get the source code of.

        Returns:
            The source code of the object as a string.

        """
        try:
            target_string = ""
            if Composer.is_config(obj):
                if SpecialKeys.TARGET in obj:
                    target_string = obj[SpecialKeys.TARGET]
            elif isinstance(obj, str):
                target_string = obj
            return UTILs.getsource(target_string) if target_string else ""
        except Exception as e:
            logger.error(f"Error getting source: {e}")
            return ""

    @staticmethod
    def viewsource(obj: Any):
        """
        Print the source code of the object.

        Args:
            obj: The object to print the source code of.

        """
        print(Composer.getsource(obj))

    @staticmethod
    def instantiate_config(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        global_package: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Instantiates an object using the provided config group and overrides.

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`)
            global_package: If True, the config assumed to be a global package
            args: Optional positional parameters pass-through
            kwargs: Optional named parameters to override
                    parameters in the config object. Parameters not present
                    in the config objects are being passed as is to the target.
                    IMPORTANT: dataclasses instances in kwargs are interpreted as config
                                and cannot be used as passthrough

        Returns:
            if _target_ is a class name: the instantiated object
            if _target_ is a callable: the return value of the call
        """
        cfg = Composer.compose(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            global_package=global_package,
        )
        return Composer.instantiate(cfg, *args, **kwargs)

    @staticmethod
    def print_config(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        global_package: bool = False,
    ):
        """
        Print the configuration

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`)
            global_package: If True, the config assumed to be a global package
        """
        cfg = Composer.compose(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            global_package=global_package,
        )
        Composer.print(cfg)

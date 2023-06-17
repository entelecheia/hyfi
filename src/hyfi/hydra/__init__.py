from typing import Any, Dict, List, Tuple, Union

import hydra
from omegaconf import DictConfig, ListConfig, OmegaConf, SCMode
from pydantic import BaseModel

from hyfi.__global__ import (
    __about__,
    __hydra_config__,
    __hydra_default_config_group_value__,
    __hydra_version_base__,
)
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


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
            config_name=self.config_name,
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
        config_name: Union[str, None] = None,
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
            config_name: Name of the root config to be used (e.g. `hconf`)
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
            config_name=config_name,
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
        config_name: Union[str, None] = None,
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
            config_name=config_name,
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
            cfg = _to_config(cfg)
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
        config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
    ):
        is_initialized = hydra.core.global_hydra.GlobalHydra.instance().is_initialized()  # type: ignore
        config_module = config_module or __hydra_config__.hyfi_config_module
        logger.debug("config_module: %s", config_module)
        if is_initialized:
            # Hydra is already initialized.
            logger.debug("Hydra is already initialized")
            cfg = hydra.compose(config_name=config_name, overrides=overrides)
        else:
            with hydra.initialize_config_module(
                config_module=config_module, version_base=__hydra_version_base__
            ):
                cfg = hydra.compose(config_name=config_name, overrides=overrides)
        if is_initialized:
            cfg = hydra.compose(config_name=config_name, overrides=overrides)
        else:
            with hydra.initialize_config_module(
                config_module=config_module, version_base=__hydra_version_base__
            ):
                cfg = hydra.compose(config_name=config_name, overrides=overrides)
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
        config_name: Union[str, None] = None,
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
                config_name=config_name,
                config_module=config_module,
                overrides=overrides,
            )
            cfg = _select(
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
        # Add config group overrides to overrides list.
        if group_key and config_data:
            for k, v in config_data.items():
                if isinstance(v, (str, int)):
                    overrides.append(f"{group_key}.{k}={v}")
        # if verbose:
        logger.debug(f"compose config with overrides: {overrides}")
        # Initialize hydra and return the configuration.
        cfg = Composer.hydra_compose(
            config_name=config_name, config_module=config_module, overrides=overrides
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


def _compose(
    config_group: Union[str, None] = None,
    overrides: Union[List[str], None] = None,
    config_data: Union[Dict[str, Any], DictConfig, None] = None,
    return_as_dict: bool = True,
    throw_on_resolution_failure: bool = True,
    throw_on_missing: bool = False,
    config_name: Union[str, None] = None,
    config_module: Union[str, None] = None,
    global_package: bool = False,
    verbose: bool = False,
) -> Union[DictConfig, Dict]:  # sourcery skip: low-code-quality
    """
    Compose a configuration by applying overrides

    Args:
        config_group: Name of the config group to compose (`config_group=name`)
        overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
        config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`)
        return_as_dict: Return the result as a dict
        throw_on_resolution_failure: If True throw an exception if resolution fails
        throw_on_missing: If True throw an exception if config_group doesn't exist
        config_name: Name of the root config to be used (e.g. `hconf`)
        config_module: Module of the config to be used (e.g. `hyfi.conf`)
        global_package: If True, the config assumed to be a global package
        verbose: If True print configuration to stdout

    Returns:
        A config object or a dictionary with the composed config
    """
    cmpsr = Composer(
        config_group=config_group,
        overrides=overrides,
        config_data=config_data,
        throw_on_resolution_failure=throw_on_resolution_failure,
        throw_on_missing=throw_on_missing,
        config_name=config_name,
        config_module=config_module,
        global_package=global_package,
        verbose=verbose,
    )
    return cmpsr.config_as_dict if return_as_dict else cmpsr.config


def _select(
    cfg: Any,
    key: str,
    default: Any = None,
    throw_on_resolution_failure: bool = True,
    throw_on_missing: bool = False,
):
    return Composer.select(
        cfg=cfg,
        key=key,
        default=default,
        throw_on_resolution_failure=throw_on_resolution_failure,
        throw_on_missing=throw_on_missing,
    )


def _to_dict(
    cfg: Any,
) -> Any:
    return Composer.to_dict(cfg)


def _to_config(
    cfg: Any,
) -> Union[DictConfig, ListConfig]:
    return Composer.to_config(cfg)

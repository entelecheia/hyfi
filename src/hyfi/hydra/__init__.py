from typing import Any, Dict, List, Union

import hydra
from omegaconf import DictConfig, ListConfig, OmegaConf, SCMode

from hyfi.__global__ import __about__, __hydra_config__, __hydra_version_base__
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


def _select(
    cfg: Any,
    key: str,
    *,
    default: Any = None,
    throw_on_resolution_failure: bool = True,
    throw_on_missing: bool = False,
):
    key = key.replace("/", ".")
    return OmegaConf.select(
        cfg,
        key=key,
        default=default,
        throw_on_resolution_failure=throw_on_resolution_failure,
        throw_on_missing=throw_on_missing,
    )


def _to_dict(
    cfg: Any,
) -> Any:
    if isinstance(cfg, dict):
        cfg = _to_config(cfg)
    if isinstance(cfg, (DictConfig, ListConfig)):
        return OmegaConf.to_container(
            cfg,
            resolve=True,
            throw_on_missing=False,
            structured_config_mode=SCMode.DICT,
        )
    return cfg


def _to_config(
    cfg: Any,
) -> Union[DictConfig, ListConfig]:
    return OmegaConf.create(cfg)


def _compose(
    config_group: Union[str, None] = None,
    overrides: Union[List[str], None] = None,
    config_data: Union[Dict[str, Any], DictConfig, None] = None,
    *,
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
    if isinstance(config_data, DictConfig):
        logger.debug("returning config_group_kwargs without composing")
        return (
            _to_dict(config_data)
            if return_as_dict and isinstance(config_data, DictConfig)
            else config_data
        )
    # Set overrides to the empty list if None
    if overrides is None:
        overrides = []
    config_module = config_module or __hydra_config__.hyfi_config_module
    # if verbose:
    logger.debug("config_module: %s", config_module)
    is_initialized = hydra.core.global_hydra.GlobalHydra.instance().is_initialized()  # type: ignore
    # Set the group key and value of the config group.
    if config_group:
        group_ = config_group.split("=")
        # group_key group_value group_key group_value group_key group_value default
        if len(group_) == 2:
            group_key, group_value = group_
        else:
            group_key = group_[0]
            group_value = "default"
        config_group = f"{group_key}={group_value}"
    else:
        group_key = None
        group_value = None
    # If group_key and group_value are specified in the configuration file.
    if group_key and group_value:
        # Initialize hydra configuration module.
        if is_initialized:
            cfg = hydra.compose(config_name=config_name, overrides=overrides)
        else:
            with hydra.initialize_config_module(
                config_module=config_module, version_base=__hydra_version_base__
            ):
                cfg = hydra.compose(config_name=config_name, overrides=overrides)
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
    if config_data:
        for k, v in config_data.items():
            if isinstance(v, (str, int)):
                overrides.append(f"{group_key}.{k}={v}")
    # if verbose:
    logger.debug(f"compose config with overrides: {overrides}")
    # Initialize hydra and return the configuration.
    if is_initialized:
        # Hydra is already initialized.
        if verbose:
            logger.debug("Hydra is already initialized")
        cfg = hydra.compose(config_name=config_name, overrides=overrides)
    else:
        with hydra.initialize_config_module(
            config_module=config_module, version_base=__hydra_version_base__
        ):
            cfg = hydra.compose(config_name=config_name, overrides=overrides)

    # Select the group_key from the configuration.
    if group_key and not global_package:
        cfg = _select(
            cfg,
            key=group_key,
            default=None,
            throw_on_missing=throw_on_missing,
            throw_on_resolution_failure=throw_on_resolution_failure,
        )
    logger.debug("Composed config: %s", OmegaConf.to_yaml(_to_dict(cfg)))
    return _to_dict(cfg) if return_as_dict and isinstance(cfg, DictConfig) else cfg

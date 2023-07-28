# Copyright (c) 2023 Massachusetts Institute of Technology
# SPDX-License-Identifier: MIT
import functools
import inspect
from pathlib import Path, PosixPath, WindowsPath
from typing import Any, Callable, Dict, FrozenSet, Optional, TypeVar

from typing_extensions import Final, ParamSpec

from hyfi.core import global_hyfi

from .composer import Composer
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

NoneType = type(None)

# Hydra-specific fields
TARGET_FIELD_NAME: Final[str] = "_target_"
PARTIAL_FIELD_NAME: Final[str] = "_partial_"
RECURSIVE_FIELD_NAME: Final[str] = "_recursive_"
CONVERT_FIELD_NAME: Final[str] = "_convert_"
POS_ARG_FIELD_NAME: Final[str] = "_args_"
DEFAULTS_LIST_FIELD_NAME: Final[str] = "defaults"

_names = [
    TARGET_FIELD_NAME,
    RECURSIVE_FIELD_NAME,
    CONVERT_FIELD_NAME,
    POS_ARG_FIELD_NAME,
    PARTIAL_FIELD_NAME,
]


HYDRA_FIELD_NAMES: FrozenSet[str] = frozenset(_names)
# Indicates types of primitive values permitted in configs
HYDRA_SUPPORTED_PRIMITIVES = frozenset(
    {
        int,
        float,
        bool,
        str,
        list,
        tuple,
        dict,
        NoneType,
        bytes,
        Path,
        PosixPath,
        WindowsPath,
    }
)

_T = TypeVar("_T")
Importable = TypeVar("Importable", bound=Callable[..., Any])
P = ParamSpec("P")
R = TypeVar("R")


_builtin_function_or_method_type = type(len)
# fmt: off
_lru_cache_type = type(functools.lru_cache(maxsize=128)(lambda: None))  # pragma: no branch
# fmt: on

_BUILTIN_TYPES: Final = (_builtin_function_or_method_type, _lru_cache_type)

del _lru_cache_type
del _builtin_function_or_method_type


class GENERATOR:
    """
    Generates Hydra configs for functions and classes.
    """

    @staticmethod
    def save_hyfi_config(
        target: Callable,
        config_name: Optional[str] = None,
        config_path: str = "run",
        config_root: Optional[str] = None,
        **kwargs_for_target,
    ) -> Dict[str, Any]:
        """
        Saves a HyFI config to a file.

        Args:
            target (Callable): The function or class to generate a config for.
            config_name (Optional[str]): The name of the config. If not provided, the name of the target will be used.
            config_path (Optional[str]): The path to save the config to (relative to the config root). Defaults to "run".
            config_root (Optional[str]): The root of the config path. If not provided, the global hyfi config directory will be used.
            **kwargs_for_target: Keyword arguments to pass to the target.
        """
        cfg = GENERATOR.generate_hyfi_config(target, **kwargs_for_target)
        filename = f"{config_name or target.__name__}.yaml"
        config_root = config_root or global_hyfi.config_root
        config_path = Path(config_root) / config_path
        config_path.mkdir(parents=True, exist_ok=True)
        config_path /= filename
        Composer.save(cfg, config_path)
        logger.info(f"Saved HyFI config for {target.__name__} to {config_path}")
        return cfg

    @staticmethod
    def generate_hyfi_config(target: Callable, **kwargs) -> Dict[str, Any]:
        params = inspect.signature(target).parameters

        config_dict = {
            "_target_": f"{target.__module__}.{target.__name__}",
        }

        for key, param in params.items():
            if key in kwargs:
                value = kwargs[key]
            else:
                value = (
                    None if param.default == inspect.Parameter.empty else param.default
                )
            config_dict[key] = sanitized_default_value(value)
        return config_dict


def sanitized_default_value(
    value: Any,
) -> Any:
    """
    Converts `value` to Hydra-supported type if necessary and possible.
    Otherwise return None.
    """
    # Common primitives supported by Hydra.
    # We check exhaustively for all Hydra-supported primitives below but seek to
    # speedup checks for common types here.
    if value is None or type(value) in {str, int, bool, float}:
        return value

    # non-str collection
    if hasattr(value, "__iter__"):
        return sanitize_collection(value)

    # importable callable (function, type, or method)
    if callable(value) and (
        inspect.isfunction(value)
        or inspect.isclass(value)
        or inspect.ismethod(value)
        or isinstance(value, _BUILTIN_TYPES)
    ):
        # `value` is importable callable -- create config that will import
        # `value` upon instantiation
        return GENERATOR.generate_hyfi_config(value)

    return None


def sanitize_collection(
    x: _T,
) -> _T:
    """Pass contents of lists, tuples, or dicts through sanitized_default_values"""
    type_x = type(x)
    if type_x in {list, tuple}:
        return type_x(sanitized_default_value(_x) for _x in x)
    elif type_x is dict:
        return {
            sanitized_default_value(k): sanitized_default_value(v) for k, v in x.items()
        }
    else:
        return None

import os
import random
from typing import Any, Callable, Dict, Union

import hydra
from omegaconf import OmegaConf

from hyfi.__global__ import __home_path__, __hyfi_path__
from hyfi.__global__.config import __global_config__, __search_package_path__
from hyfi.cached_path import cached_path
from hyfi.composer import Composer, SpecialKeys
from hyfi.utils.envs import ENVs
from hyfi.utils.funcs import FUNCs
from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING
from hyfi.utils.packages import PKGs

logger = LOGGING.getLogger(__name__)


class XC(Composer):
    """
    Extended Composer class
    """

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
            config = XC.to_dict(config)
        if not isinstance(config, dict):
            raise ValueError("config must be a dict or a str")
        config[SpecialKeys.PARTIAL.value] = True
        rc_kwargs_ = config.pop(SpecialKeys.KWARGS, {})
        if rc_kwargs_ and kwargs:
            kwargs.update(rc_kwargs_)
        return XC.instantiate(config, *args, **kwargs)

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
        if not __global_config__._initilized_:
            __global_config__.initialize()
        if not XC.is_instantiatable(config):
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
            if XC.is_config(obj):
                if SpecialKeys.TARGET in obj:
                    target_string = obj[SpecialKeys.TARGET]
            elif isinstance(obj, str):
                target_string = obj
            return PKGs.getsource(target_string) if target_string else ""
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
        print(XC.getsource(obj))


OmegaConf.register_new_resolver("__hyfi_path__", __hyfi_path__)
OmegaConf.register_new_resolver("__search_package_path__", __search_package_path__)
OmegaConf.register_new_resolver("__home_path__", __home_path__)
OmegaConf.register_new_resolver("today", FUNCs.today)
OmegaConf.register_new_resolver("to_datetime", FUNCs.strptime)
OmegaConf.register_new_resolver("iif", lambda cond, t, f: t if cond else f)
OmegaConf.register_new_resolver("alt", lambda val, alt: val or alt)
OmegaConf.register_new_resolver("randint", random.randint, use_cache=True)
OmegaConf.register_new_resolver("get_method", hydra.utils.get_method)
OmegaConf.register_new_resolver("get_original_cwd", ENVs.getcwd)
OmegaConf.register_new_resolver("exists", IOLIBs.exists)
OmegaConf.register_new_resolver("join_path", IOLIBs.join_path)
OmegaConf.register_new_resolver("mkdir", IOLIBs.mkdir)
OmegaConf.register_new_resolver("dirname", os.path.dirname)
OmegaConf.register_new_resolver("basename", os.path.basename)
OmegaConf.register_new_resolver("check_path", IOLIBs.check_path)
OmegaConf.register_new_resolver("cached_path", cached_path)
OmegaConf.register_new_resolver(
    "lower_case_with_underscores", FUNCs.lower_case_with_underscores
)
OmegaConf.register_new_resolver("dotenv_values", ENVs.dotenv_values)

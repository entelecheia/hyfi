import importlib
import inspect
import os
import random
from typing import Any, Callable, Dict, Union

import hydra
from omegaconf import OmegaConf

from hyfi.__global__ import __home_path__, __hyfi_path__
from hyfi.__global__.config import __global_config__, __search_package_path__
from hyfi.cached_path import cached_path
from hyfi.composer import Composer, SpecialKeys
from hyfi.utils.envs import Envs
from hyfi.utils.funcs import Funcs
from hyfi.utils.iolibs import IOLibs
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


# _config_ = XC.config.copy()


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
        if isinstance(config, str):
            config = {SpecialKeys.TARGET.value: config}
        else:
            config = XC.to_dict(config)
        config[SpecialKeys.PARTIAL.value] = True
        rcParams = config.pop(SpecialKeys.rcPARAMS, {})
        if rcParams and kwargs:
            kwargs = kwargs.update(rcParams)
        return XC.instantiate(config, *args, **kwargs)

    @staticmethod
    def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
        """
        :param config: An config object describing what to call and what params to use.
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
        :param args: Optional positional parameters pass-through
        :param kwargs: Optional named parameters to override
                    parameters in the config object. Parameters not present
                    in the config objects are being passed as is to the target.
                    IMPORTANT: dataclasses instances in kwargs are interpreted as config
                                and cannot be used as passthrough
        :return: if _target_ is a class name: the instantiated object
                if _target_ is a callable: the return value of the call
        """
        verbose = config.get(SpecialKeys.VERBOSE, False)
        if not __global_config__.__initilized__:
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
    def run(config: Any, **kwargs: Any) -> Any:
        config = XC.merge(config, kwargs)
        _config_ = config.get(SpecialKeys.CONFIG)
        if _config_ is None:
            logger.warning("No _config_ specified in config")
            return None
        if isinstance(_config_, str):
            _config_ = [_config_]
        for _cfg_ in _config_:
            cfg = XC.select(config, _cfg_)
            XC.instantiate(cfg)

    @staticmethod
    def function(cfg: Any, _name_, return_function=False, **parms):
        cfg = XC.to_dict(cfg)
        if not isinstance(cfg, dict):
            logger.info("No function defined to execute")
            return None

        if SpecialKeys.FUNC not in cfg:
            logger.info("No function defined to execute")
            return None

        _functions_ = cfg[SpecialKeys.FUNC]
        fn = XC.partial(_functions_[_name_])
        if _name_ in cfg:
            _parms = cfg[_name_]
            _parms = {**_parms, **parms}
        else:
            _parms = parms
        _exec_ = _parms.pop(SpecialKeys.EXEC) if SpecialKeys.EXEC in _parms else True
        if _exec_:
            if callable(fn):
                if return_function:
                    logger.info(f"Returning function {fn}")
                    return fn
                logger.info(f"Executing function {fn} with parms {_parms}")
                return fn(**_parms)
            else:
                logger.info(f"Function {_name_} not callable")
                return None
        else:
            logger.info(f"Skipping execute of {fn}")
            return None

    @staticmethod
    def getsource(obj):
        """Return the source code of the object."""
        try:
            if XC.is_config(obj):
                if SpecialKeys.TARGET in obj:
                    target_string = obj[SpecialKeys.TARGET]
                    mod_name, object_name = target_string.rsplit(".", 1)
                    mod = importlib.import_module(mod_name)
                    obj = getattr(mod, object_name)
            elif isinstance(obj, str):
                mod_name, object_name = obj.rsplit(".", 1)
                mod = importlib.import_module(mod_name)
                obj = getattr(mod, object_name)
            return inspect.getsource(obj)
        except Exception as e:
            logger.error(f"Error getting source: {e}")
            return ""

    @staticmethod
    def viewsource(obj):
        """Print the source code of the object."""
        print(XC.getsource(obj))


OmegaConf.register_new_resolver("__hyfi_path__", __hyfi_path__)
OmegaConf.register_new_resolver("__search_package_path__", __search_package_path__)
OmegaConf.register_new_resolver("__home_path__", __home_path__)
OmegaConf.register_new_resolver("today", Funcs.today)
OmegaConf.register_new_resolver("to_datetime", Funcs.strptime)
OmegaConf.register_new_resolver("iif", lambda cond, t, f: t if cond else f)
OmegaConf.register_new_resolver("alt", lambda val, alt: val or alt)
OmegaConf.register_new_resolver("randint", random.randint, use_cache=True)
OmegaConf.register_new_resolver("get_method", hydra.utils.get_method)
OmegaConf.register_new_resolver("get_original_cwd", Envs.getcwd)
OmegaConf.register_new_resolver("exists", IOLibs.exists)
OmegaConf.register_new_resolver("join_path", IOLibs.join_path)
OmegaConf.register_new_resolver("mkdir", IOLibs.mkdir)
OmegaConf.register_new_resolver("dirname", os.path.dirname)
OmegaConf.register_new_resolver("basename", os.path.basename)
OmegaConf.register_new_resolver("check_path", IOLibs.check_path)
OmegaConf.register_new_resolver("cached_path", cached_path)
OmegaConf.register_new_resolver(
    "lower_case_with_underscores", Funcs.lower_case_with_underscores
)
OmegaConf.register_new_resolver("dotenv_values", Envs.dotenv_values)

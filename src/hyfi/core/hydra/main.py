# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
from textwrap import dedent
from typing import Any, Callable, Optional

from hydra import version
from hydra._internal.deprecation_warning import deprecation_warning
from hydra._internal.utils import get_args_parser
from hydra.core.utils import _flush_loggers
from hydra.main import _get_rerun_conf
from hydra.types import TaskFunction
from omegaconf import DictConfig

from hyfi.core.hydra.utils import _run_hydra

_UNSPECIFIED_: Any = object()


def main(
    config_path: Optional[str] = _UNSPECIFIED_,
    config_name: Optional[str] = None,
    version_base: Optional[str] = _UNSPECIFIED_,
) -> Callable[[TaskFunction], Any]:
    """
    :param config_path: The config path, a directory where Hydra will search for
                        config files. This path is added to Hydra's searchpath.
                        Relative paths are interpreted relative to the declaring python
                        file. Alternatively, you can use the prefix `pkg://` to specify
                        a python package to add to the searchpath.
                        If config_path is None no directory is added to the Config search path.
    :param config_name: The name of the config (usually the file name without the .yaml extension)
    """

    version.setbase(version_base)

    if config_path is _UNSPECIFIED_:
        if version.base_at_least("1.2"):
            config_path = None
        elif version_base is _UNSPECIFIED_:
            url = "https://hydra.cc/docs/1.2/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"
            deprecation_warning(
                message=dedent(
                    f"""
                config_path is not specified in @hydra.main().
                See {url} for more information."""
                ),
                stacklevel=2,
            )
            config_path = "."
        else:
            config_path = "."

    def main_decorator(task_function: TaskFunction) -> Callable[[], None]:
        @functools.wraps(task_function)
        def decorated_main(cfg_passthrough: Optional[DictConfig] = None) -> Any:
            if cfg_passthrough is not None:
                return task_function(cfg_passthrough)
            args_parser = get_args_parser()
            args = args_parser.parse_args()
            if args.experimental_rerun is not None:
                cfg = _get_rerun_conf(args.experimental_rerun, args.overrides)
                task_function(cfg)
                _flush_loggers()
            else:
                # no return value from run_hydra() as it may sometime actually run the task_function
                # multiple times (--multirun)
                _run_hydra(
                    args=args,
                    args_parser=args_parser,
                    task_function=task_function,
                    config_path=config_path,
                    config_name=config_name,
                )

        return decorated_main

    return main_decorator

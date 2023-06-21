"""
    Pipeline Functions
"""
from typing import Any, Dict, Union

import pandas as pd

from hyfi.composer.extended import XC
from hyfi.pipe import PIPE, PipeConfig
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


def apply_pipe_func(data: Any, pipe_config: Union[Dict, PipeConfig]):
    if isinstance(pipe_config, dict):
        pipe_config = PipeConfig(**pipe_config)
    if not pipe_config._method_:
        raise ValueError("No method specified")
    if pipe_config._type_ == "instance":
        apply_fn_ = apply_instance_methods
    else:
        apply_fn_ = apply_external_funcs
    if pipe_config.verbose:
        logger.info("Running dataframe function: %s", pipe_config)
    if isinstance(data, dict):
        dfs = {}
        for df_no, df_name in enumerate(data):
            df = data[df_name]

            logger.info(
                "Applying pipe to dataframe [%s], %d/%d",
                df_name,
                df_no + 1,
                len(data),
            )

            dfs[df_name] = apply_fn_(df, pipe_config)
        return dfs

    return apply_fn_(data, pipe_config)


def apply_instance_methods(data: pd.DataFrame, config: PipeConfig):
    with elapsed_timer(format_time=True) as elapsed:
        if config.apply_to:
            if isinstance(config.apply_to, str):
                config.apply_to = [config.apply_to]
            for key in config.apply_to:
                logger.info("processing column: %s", key)
                data[key] = getattr(data[key], config._method_)(**config.rcParams)
        else:
            data = getattr(data, config._method_)(**config.rcParams)

        logger.info(" >> elapsed time to replace: %s", elapsed())
        if config.verbose:
            print(data.head())
    return data


def apply_external_funcs(data: pd.DataFrame, config: PipeConfig):
    if config._type_ == "lambda":
        _fn = eval(config._method_)
    else:
        _fn = XC.partial(config._method_, **config.rcParams)
    with elapsed_timer(format_time=True) as elapsed:
        if config.apply_to:
            if isinstance(config.apply_to, str):
                config.apply_to = [config.apply_to]
            for key in config.apply_to:
                logger.info("processing column: %s", key)
                data[key] = PIPE.apply(
                    _fn,
                    data[key],
                    use_batcher=config.use_batcher,
                    num_workers=config.num_workers,
                )
        else:
            data = PIPE.apply(
                _fn,
                data,
                use_batcher=config.use_batcher,
                num_workers=config.num_workers,
            )

        logger.info(" >> elapsed time to replace: %s", elapsed())
        if config.verbose:
            print(data.head())
    return data

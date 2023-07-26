"""
    Pipeline Functions
"""
from typing import Any

import pandas as pd

from hyfi.joblib import BATCHER
from hyfi.pipeline.configs import DataframePipeConfig, PipeConfig
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


def general_instance_methods(obj: Any, config: PipeConfig):
    """
    Applies a general instance method to an object.

    Args:
        obj (Any): The object to apply the method to.
        config (PipeConfig): The configuration for the pipeline.

    Returns:
        Any: The object with the method applied.
    """
    run_target = config.run_target
    run_kwargs = config.run_kwargs
    if not run_target:
        logger.warning("No target found for %s", config)
        return obj
    with elapsed_timer(format_time=True) as elapsed:
        obj = getattr(obj, run_target)(**run_kwargs)

        if config.verbose:
            logger.info(" >> elapsed time: %s", elapsed())
    return obj


def general_external_funcs(obj: Any, config: PipeConfig):
    """
    Applies a general external function to an object.

    Args:
        obj (Any): The object to apply the function to.
        config (PipeConfig): The configuration for the pipeline.

    Returns:
        Any: The object with the function applied.
    """
    _fn = config.get_run_func()
    if _fn is None:
        logger.warning("No function found for %s", config)
        return obj
    with elapsed_timer(format_time=True) as elapsed:
        obj_arg = (
            {config.pipe_obj_arg_name: obj}
            if config.pipe_obj_arg_name and config.use_pipe_obj
            else {}
        )
        obj_ = (
            _fn(**obj_arg)
            if obj_arg
            else _fn(obj)
            if obj is not None and config.use_pipe_obj
            else _fn()
        )
        # return original data if no return value to continue pipeline
        obj = obj if config.return_pipe_obj or obj_ is None else obj_
        if config.verbose:
            logger.info(" >> elapsed time: %s", elapsed())
    return obj


def dataframe_instance_methods(data: pd.DataFrame, config: DataframePipeConfig):
    """
    Applies a dataframe instance method to a dataframe.

    Args:
        data (pd.DataFrame): The dataframe to apply the method to.
        config (DataframePipeConfig): The configuration for the pipeline.

    Returns:
        pd.DataFrame: The dataframe with the method applied.
    """
    config = DataframePipeConfig(**config.model_dump())
    run_target = config.run_target
    run_kwargs = config.run_kwargs
    if not run_target:
        logger.warning("No target found for %s", config)
        return data
    with elapsed_timer(format_time=True) as elapsed:
        if config.columns:
            for col_name in config.columns:
                logger.info("processing column: %s", col_name)
                data[col_name] = getattr(data[col_name], run_target)(**run_kwargs)
        else:
            data = getattr(data, run_target)(**run_kwargs)

        if config.verbose:
            logger.info(" >> elapsed time: %s", elapsed())
            print(data.head())
    return data


def dataframe_external_funcs(data: pd.DataFrame, config: DataframePipeConfig):
    """
    Applies a dataframe external function to a dataframe.

    Args:
        data (pd.DataFrame): The dataframe to apply the function to.
        config (DataframePipeConfig): The configuration for the pipeline.

    Returns:
        pd.DataFrame: The dataframe with the function applied.
    """
    config = DataframePipeConfig(**config.model_dump())
    _fn = config.get_run_func()
    if _fn is None:
        logger.warning("No function found for %s", config)
        return data
    with elapsed_timer(format_time=True) as elapsed:
        if config.columns:
            for key in config.columns:
                logger.info("processing column: %s", key)
                data[key] = (
                    BATCHER.apply(
                        _fn,
                        data[key],
                        use_batcher=config.use_batcher,
                        num_workers=config.num_workers,
                    )
                    if config.use_batcher
                    else data[key].apply(_fn)
                )
        elif config.use_batcher:
            data_ = BATCHER.apply(
                _fn,
                data,
                use_batcher=config.use_batcher,
                num_workers=config.num_workers,
            )
            # return original data if no return value to continue pipeline
            data = data if config.return_pipe_obj or data_ is None else data_
        else:
            data_arg = (
                {config.pipe_obj_arg_name: data}
                if config.pipe_obj_arg_name and config.use_pipe_obj
                else {}
            )
            data_ = (
                _fn(**data_arg)
                if data_arg
                else _fn(data)
                if data is not None and config.use_pipe_obj
                else _fn()
            )
            # return original data if no return value to continue pipeline
            data = data if config.return_pipe_obj or data_ is None else data_
        if config.verbose:
            logger.info(" >> elapsed time: %s", elapsed())
            print(data.head())
    return data

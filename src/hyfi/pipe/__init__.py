"""
    Pipeline Functions
"""
import pandas as pd

from hyfi.joblib import BATCHER
from hyfi.pipeline.configs import DataframePipeConfig
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


def dataframe_instance_methods(data: pd.DataFrame, config: DataframePipeConfig):
    config = DataframePipeConfig(**config.dict())
    with elapsed_timer(format_time=True) as elapsed:
        if config.columns:
            for col_name in config.columns:
                logger.info("processing column: %s", col_name)
                data[col_name] = getattr(data[col_name], config._run_)(**config.kwargs)
        else:
            data = getattr(data, config._run_)(**config.kwargs)

        if config.verbose:
            logger.info(" >> elapsed time: %s", elapsed())
            print(data.head())
    return data


def dataframe_external_funcs(data: pd.DataFrame, config: DataframePipeConfig):
    config = DataframePipeConfig(**config.dict())
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
            data = data_ if data_ is not None else data
        else:
            data_arg = (
                {config.pipe_obj_arg_name: data} if config.pipe_obj_arg_name else {}
            )
            data_ = (
                _fn(**data_arg)
                if data_arg
                else _fn(data)
                if data is not None
                else _fn()
            )
            # return original data if no return value to continue pipeline
            data = data_ if data_ is not None else data
        if config.verbose:
            logger.info(" >> elapsed time: %s", elapsed())
            print(data.head())
    return data

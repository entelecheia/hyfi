"""
    Pipeline Functions
"""
from typing import Any, Dict

import pandas as pd

from hyfi.pipe import PipeConfig
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


def data_class_methods(data: Any, config_kwargs: Dict):
    config = PipeConfig(**config_kwargs)
    if config.verbose:
        logger.info("Running dataframe function: %s", config_kwargs)
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

            dfs[df_name] = dataframe_class_methods(df, config_kwargs)
        return dfs

    return dataframe_class_methods(data, config_kwargs)


def dataframe_class_methods(data: pd.DataFrame, config: PipeConfig):
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

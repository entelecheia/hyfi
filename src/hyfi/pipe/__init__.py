"""
    Pipeline Functions
"""
import pandas as pd

from hyfi.joblib import BATCHER
from hyfi.pipeline.configs import DataframeRunConfig
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


def dataframe_instance_methods(data: pd.DataFrame, rc: DataframeRunConfig):
    rc = DataframeRunConfig(**rc.dict())
    with elapsed_timer(format_time=True) as elapsed:
        if rc.columns:
            for col_name in rc.columns:
                logger.info("processing column: %s", col_name)
                data[col_name] = getattr(data[col_name], rc._target_)(**rc.kwargs)
        else:
            data = getattr(data, rc._target_)(**rc.kwargs)

        logger.info(" >> elapsed time to replace: %s", elapsed())
        if rc.verbose:
            print(data.head())
    return data


def dataframe_external_funcs(data: pd.DataFrame, rc: DataframeRunConfig):
    rc = DataframeRunConfig(**rc.dict())
    _fn = rc.get_func()
    if _fn is None:
        logger.warning("No function found for %s", rc)
        return data
    with elapsed_timer(format_time=True) as elapsed:
        if rc.columns:
            for key in rc.columns:
                logger.info("processing column: %s", key)
                data[key] = (
                    BATCHER.apply(
                        _fn,
                        data[key],
                        use_batcher=rc.use_batcher,
                        num_workers=rc.num_workers,
                    )
                    if rc.use_batcher
                    else data[key].apply(_fn)
                )
        elif rc.use_batcher:
            data = BATCHER.apply(
                _fn,
                data,
                use_batcher=rc.use_batcher,
                num_workers=rc.num_workers,
            )
        else:
            data = _fn(data) if data is not None else _fn()
        logger.info(" >> elapsed time to replace: %s", elapsed())
        if rc.verbose:
            print(data.head())
    return data

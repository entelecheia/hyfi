"""
A class to apply a pipe to a dataframe or a dictionary of dataframes.
"""
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Union

import pandas as pd
from pydantic import validator
from tqdm.auto import tqdm

from hyfi.composer import BaseConfig
from hyfi.composer.extended import XC
from hyfi.joblib import JobLibConfig
from hyfi.joblib.batch.apply import decorator_apply
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


class PipeConfig(BaseConfig):
    """Pipe Configuration"""

    config_name: str = "__init__"
    config_group: str = "pipe"

    _func_: Union[str, Dict] = "hyfi.pipe.funcs.apply_pipe_func"
    _type_: str = "instance"
    _method_: str = ""
    apply_to: Union[str, List[str], None] = "text"
    rcParams: Optional[Dict[str, Any]] = None
    use_batcher: bool = True
    num_workers: Optional[int] = 1
    verbose: bool = False

    class Config:
        underscore_attrs_are_private = False

    @validator("rcParams", pre=True, always=True)
    def _validate_rcParams(cls, v):
        return {} if v is None else v


class PIPE:
    """
    A class to apply a pipe to a dataframe or a dictionary of dataframes.
    """

    @staticmethod
    def pipe(data: Any, pipe_config: Union[Dict, PipeConfig]):
        if isinstance(pipe_config, dict):
            pipe_config = PipeConfig(**pipe_config)
        _func_ = pipe_config._func_
        _fn = XC.partial(_func_)
        logger.info("Applying pipe: %s", _fn)
        return _fn(data, pipe_config)

    @staticmethod
    def apply(
        func: Callable,
        series: Union[pd.Series, pd.DataFrame, Sequence, Mapping],
        description: Optional[str] = None,
        use_batcher: bool = True,
        minibatch_size: Optional[int] = None,
        num_workers: Optional[int] = None,
        **kwargs,
    ):
        batcher_instance = JobLibConfig().__batcher_instance__
        if use_batcher and batcher_instance is not None:
            batcher_minibatch_size = batcher_instance.minibatch_size
            if minibatch_size is None:
                minibatch_size = batcher_minibatch_size
            if num_workers is not None:
                batcher_instance.procs = int(num_workers)
            if batcher_instance.procs > 1:
                batcher_instance.minibatch_size = min(
                    int(len(series) / batcher_instance.procs) + 1, minibatch_size
                )
                logger.info(
                    f"Using batcher with minibatch size: {batcher_instance.minibatch_size}"
                )
                results = decorator_apply(
                    func,
                    batcher_instance,
                    description=description,  # type: ignore
                )(series)
                if batcher_instance is not None:
                    batcher_instance.minibatch_size = batcher_minibatch_size
                return results

        if batcher_instance is None:
            logger.info("Warning: batcher not initialized")
        tqdm.pandas(desc=description)
        return series.progress_apply(func)

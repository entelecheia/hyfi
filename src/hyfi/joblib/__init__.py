from typing import Callable, Mapping, Optional, Sequence, Union

import pandas as pd
from pydantic import BaseModel, PrivateAttr
from tqdm.auto import tqdm

from hyfi import __global__
from hyfi.composer import BaseConfig
from hyfi.joblib.batch import batcher
from hyfi.joblib.batch.apply import decorator_apply
from hyfi.joblib.batch.batcher import Batcher
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class DistFramworkConfig(BaseModel):
    """Distributed Framework Configuration"""

    backend: str = "joblib"
    initialize: bool = False
    num_workers: int = 1


class BatcherConfig(BaseModel):
    """Batcher Configuration"""

    procs: int = 1
    minibatch_size: int = 1_000
    backend: str = "joblib"
    task_num_cpus: int = 1
    task_num_gpus: int = 0
    verbose: int = 10


class JobLibConfig(BaseConfig):
    """JobLib Configuration"""

    _config_name_: str = "__init__"
    _config_group_: str = "joblib"

    num_workers: int = 1
    distributed_framework: DistFramworkConfig = DistFramworkConfig()
    batcher: BatcherConfig = BatcherConfig()
    _initilized_: bool = PrivateAttr(False)
    _batcher_instance_: Optional[Batcher] = PrivateAttr(None)

    def initialize(self):
        self.init_backend()

    def init_backend(
        self,
    ):
        """Initialize the backend for joblib"""
        if self.distributed_framework.initialize:
            backend_handle = None
            backend = self.distributed_framework.backend

            if backend == "ray":
                import ray  # type: ignore

                ray_cfg = {"num_cpus": self.distributed_framework.num_workers}
                logger.debug(f"initializing ray with {ray_cfg}")
                ray.init(**ray_cfg)
                backend_handle = ray

            __global__._batcher_instance_ = batcher.Batcher(
                backend_handle=backend_handle, **self.batcher.model_dump()
            )
            self._batcher_instance_ = __global__._batcher_instance_
            logger.debug("initialized batcher with %s", __global__._batcher_instance_)
        self._initilized_ = True

    def stop_backend(self):
        """Stop the backend for joblib"""
        backend = self.distributed_framework.backend
        if __global__._batcher_instance_:
            logger.debug("stopping batcher")
            del __global__._batcher_instance_

        logger.debug("stopping distributed framework")
        if self.distributed_framework.initialize and backend == "ray":
            try:
                import ray  # type: ignore

                if ray.is_initialized():
                    ray.shutdown()
                    logger.debug("shutting down ray")
            except ImportError:
                logger.warning("ray is not installed")


class BATCHER:
    """
    A class to apply a function to a series or dataframe using joblib
    """

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
        batcher_instance = JobLibConfig()._batcher_instance_
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
        return series.progress_apply(func)  # type: ignore

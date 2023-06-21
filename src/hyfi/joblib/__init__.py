from typing import Any

from pydantic import BaseModel

from hyfi import __global__
from hyfi.composer import BaseConfig
from hyfi.joblib.batch import batcher
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


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

    config_name: str = "__init__"
    config_group: str = "joblib"

    num_workers: int = 1
    distributed_framework: DistFramworkConfig = DistFramworkConfig()
    batcher: BatcherConfig = BatcherConfig()
    __initilized__: bool = False
    __batcher_instance__: Any = None

    class Config:
        extra = "allow"
        underscore_attrs_are_private = True

    def initialize_configs(self, **config_kwargs):
        super().initialize_configs(**config_kwargs)
        self.batcher = BatcherConfig.parse_obj(self.__dict__["batcher"])
        self.distributed_framework = DistFramworkConfig.parse_obj(
            self.__dict__["distributed_framework"]
        )
        self.init_backend()

    def init_backend(
        self,
    ):
        """Initialize the backend for joblib"""
        if self.distributed_framework.initialize:
            backend_handle = None
            backend = self.distributed_framework.backend

            if backend == "dask":
                from dask.distributed import Client  # type: ignore

                dask_cfg = {"n_workers": self.distributed_framework.num_workers}
                logger.debug(f"initializing dask client with {dask_cfg}")
                client = Client(**dask_cfg)
                logger.debug(client)

            elif backend == "ray":
                import ray  # type: ignore

                ray_cfg = {"num_cpus": self.distributed_framework.num_workers}
                logger.debug(f"initializing ray with {ray_cfg}")
                ray.init(**ray_cfg)
                backend_handle = ray

            __global__.__batcher_instance__ = batcher.Batcher(
                backend_handle=backend_handle, **self.batcher.dict()
            )
            self.__batcher_instance__ = __global__.__batcher_instance__
            logger.debug("initialized batcher with %s", __global__.__batcher_instance__)
        self.__initilized__ = True

    def stop_backend(self):
        """Stop the backend for joblib"""
        backend = self.distributed_framework.backend
        if __global__.__batcher_instance__:
            logger.debug("stopping batcher")
            del __global__.__batcher_instance__

        logger.debug("stopping distributed framework")
        if self.distributed_framework.initialize:
            if backend == "ray":
                try:
                    import ray  # type: ignore

                    if ray.is_initialized():
                        ray.shutdown()
                        logger.debug("shutting down ray")
                except ImportError:
                    logger.warning("ray is not installed")

            elif backend == "dask":
                try:
                    from dask.distributed import Client  # type: ignore

                    if Client.initialized():
                        Client.close()
                        logger.debug("shutting down dask client")
                except ImportError:
                    logger.warning("dask is not installed")

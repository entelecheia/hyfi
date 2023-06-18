from typing import Any

from pydantic import BaseModel

from hyfi.__global__ import __about__
from hyfi.hydra import Composer
from hyfi.joblib.batch import batcher
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


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


class JobLibConfig(BaseModel):
    """JobLib Configuration"""

    config_name: str = "__init__"
    num_workers: int = 1
    distributed_framework: DistFramworkConfig = DistFramworkConfig()
    batcher: BatcherConfig = BatcherConfig()
    __initilized__: bool = False

    class Config:
        extra = "allow"
        underscore_attrs_are_private = True

    def __init__(
        self,
        config_name: str = "__init__",
        config_group: str = "joblib",
        **data: Any,
    ):
        """
        Initialize the config. This is the base implementation of __init__.
        You can override this in your own subclass if you want to customize the initilization of a config by passing a keyword argument ` data `.

        Args:
                config_name: The name of the config to initialize
                data: The data to initialize
        """
        super().__init__(**data)
        self.initialize_configs(
            config_name=config_name,
            config_group=config_group,
            **data,
        )

    def initialize_configs(
        self,
        config_name: str = "__init__",
        config_group: str = "joblib",
        **data,
    ):
        # Initialize the config with the given config_name.
        data = Composer(
            config_group=f"{config_group}={config_name}",
            config_data=data,
        ).config_as_dict
        self.__dict__.update(data)
        self.distributed_framework = DistFramworkConfig(**self.__dict__["distributed_framework"])
        self.batcher = BatcherConfig(**self.__dict__["batcher"])

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

            batcher.batcher_instance = batcher.Batcher(
                backend_handle=backend_handle, **self.batcher.dict()
            )
            logger.debug(f"initialized batcher with {batcher.batcher_instance}")
        self.__initilized__ = True

    def stop_backend(self):
        """Stop the backend for joblib"""
        backend = self.distributed_framework.backend
        if batcher.batcher_instance:
            logger.debug("stopping batcher")
            del batcher.batcher_instance

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

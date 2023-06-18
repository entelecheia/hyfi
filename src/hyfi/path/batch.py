from pathlib import Path
from typing import Any

from hyfi.hydra import Composer
from hyfi.path.task import TaskPathConfig
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


class BatchPathConfig(TaskPathConfig):
    config_name: str = "__batch__"

    batch_outputs: str = ""

    class Config:
        extra = "ignore"

    def __init__(
        self,
        config_name: str = "__batch__",
        config_group: str = "path",
        **data: Any,
    ):
        """
        Initialize the batch. This is the method you call when you want to initialize the batch from a config

        Args:
            config_name: The name of the config you want to use
            data: The data you want to initilize the
        """
        # Initialize the config with the given config_name.
        super().__init__(**data)
        self.initialize_configs(
            config_name=config_name,
            config_group=config_group,
            **data,
        )

    def initialize_configs(
        self,
        config_name: str = "__batch__",
        config_group: str = "path",
        **data,
    ):
        # Initialize the config with the given config_name.
        data = Composer(
            config_group=f"{config_group}={config_name}",
            config_data=data,
        ).config_as_dict
        self.__dict__.update(data)

    @property
    def batch_dir(self) -> Path:
        """
        The directory where the batch is stored. It is used to determine where the results are stored for a batch of data to be processed.


        Returns:
                The directory where the batch output is stored for a batch of data to be processed ( relative to the task output directory )
        """
        self.batch_outputs = (
            self.batch_outputs or (self.output_dir / "batch-outputs").as_posix()
        )
        return Path(self.batch_outputs).absolute()

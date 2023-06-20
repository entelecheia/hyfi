from pathlib import Path

from hyfi.path.task import TaskPathConfig
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


class BatchPathConfig(TaskPathConfig):
    config_name: str = "__batch__"
    config_group: str = "path"

    batch_outputs: str = ""

    class Config:
        extra = "ignore"

    def initialize_configs(self, **config_kwargs):
        super().initialize_configs(**config_kwargs)

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

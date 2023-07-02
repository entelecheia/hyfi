from pathlib import Path

from hyfi.path.task import TaskPathConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BatchPathConfig(TaskPathConfig):
    _config_name_: str = "__batch__"
    _config_group_: str = "path"

    batch_name: str = "demo-batch"

    @property
    def batch_dir(self) -> Path:
        """
        The directory where the batch is stored. It is used to determine where the results are stored for a batch of data to be processed.

        Returns:
                The directory where the batch output is stored for a batch of data to be processed ( relative to the task output directory )
        """
        path_ = self.output_dir / self.batch_name
        path_.mkdir(parents=True, exist_ok=True)
        return path_

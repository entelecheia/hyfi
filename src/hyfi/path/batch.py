from pathlib import Path

from hyfi.utils.logging import LOGGING

from .task import TaskPathConfig

logger = LOGGING.getLogger(__name__)


class BatchPathConfig(TaskPathConfig):
    _config_name_: str = "__batch__"

    batch_name: str = "demo-batch"

    @property
    def batch_dir(self) -> Path:
        """
        Returns the path to the batch directory.
        """
        path_ = self.task_dir / self.batch_name
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def workspace_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        return self.batch_dir

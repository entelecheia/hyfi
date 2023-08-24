from pathlib import Path

from hyfi.utils.logging import LOGGING

from .task import TaskPath

logger = LOGGING.getLogger(__name__)


class BatchPath(TaskPath):
    _config_name_: str = "__batch__"

    batch_name: str = "demo-batch"

    @property
    def batch_dir(self) -> Path:
        """
        Returns the path to the batch directory.
        """
        return self.task_dir / self.batch_name

    @property
    def workspace_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        return self.batch_dir

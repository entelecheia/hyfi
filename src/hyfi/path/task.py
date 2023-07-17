from pathlib import Path

from hyfi.path.base import BasePathConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class TaskPathConfig(BasePathConfig):
    task_name: str = "demo-task"
    task_root: str = "workspace"

    @property
    def name(self) -> str:
        """
        Returns the name of the path configuration.
        """
        return self.task_name

    @property
    def root_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        # return as an path
        path_ = Path(self.task_root)
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def task_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        # return as an path
        path_ = self.root_dir / self.task_name
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def workspace_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        return self.root_dir

from pathlib import Path

from hyfi.main.config import global_config
from hyfi.utils.logging import LOGGING

from .base import BasePath

logger = LOGGING.getLogger(__name__)

__default_task_name__ = "demo-task"
__default_task_root__ = "workspace"


class TaskPath(BasePath):
    _config_name_: str = "__task__"

    task_name: str = __default_task_name__
    task_root: str = __default_task_root__

    @property
    def name(self) -> str:
        """
        Returns the name of the path configuration.
        """
        return self.task_name

    @property
    def project_dir(self) -> Path:
        return global_config.project_dir

    @property
    def project_workspace_dir(self) -> Path:
        return global_config.project_workspace_dir

    @property
    def root_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        # return as an path
        if self.task_root == __default_task_root__:
            path_ = self.project_workspace_dir
        else:
            path_ = Path(self.task_root)
            if not path_.is_absolute():
                path_ = self.project_dir / path_
        return path_.absolute()

    @property
    def task_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        return self.root_dir / self.task_name

    @property
    def workspace_dir(self) -> Path:
        """
        Returns the path to the task root directory.

        Returns:
            an path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        return self.root_dir

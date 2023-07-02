from pathlib import Path

from hyfi.composer import BaseConfig
from hyfi.path.dirnames import DirnamesConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class TaskPathConfig(BaseConfig):
    _config_name_: str = "__task__"
    _config_group_: str = "path"

    task_name: str = "demo-task"
    task_root: str = "workspace/tasks"
    dirnames: DirnamesConfig = DirnamesConfig()

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
    def input_dir(self) -> Path:
        """
        Returns the directory where the task inputs are stored.
        It is used to determine where the input files will be loaded from when running the task.

        Returns:
            path to the input directory of the task ( relative to the task root directory ) or None if not
        """
        path_ = self.task_dir / self.dirnames.inputs
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def output_dir(self) -> Path:
        """
        Returns the directory where the task outputs are stored.
        It is used to determine where the output files will be stored when running the task.

        Returns:
            path to the output directory of the task ( relative to the task root directory ) or None if not
        """
        path_ = self.task_dir / self.dirnames.outputs
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def library_dir(self) -> Path:
        """
        The path to the library.

        Returns:
            path to the library directory ( relative to the task root directory ).
        """
        path_ = self.task_dir / self.dirnames.library
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def dataset_dir(self) -> Path:
        """
        Get the path to the dataset directory.


        Returns:
            path to the dataset directory ( relative to the root directory ) or None if not set in the
        """
        path_ = self.task_dir / self.dirnames.datasets
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def model_dir(self) -> Path:
        """
        Get the directory where models are stored.


        Returns:
            path to the models directory on the task's filesystem ( relative to the root_dir )
        """
        path_ = self.task_dir / self.dirnames.models
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def cache_dir(self) -> Path:
        """
        The directory where tasks are cached.


        Returns:
            A path to the cache directory for this task or None if it is not set in the config
        """
        path_ = self.task_dir / self.dirnames.cache
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def tmp_dir(self) -> Path:
        """
        Returns the path to the temporary directory.

        Returns:
            path to the temporary directory of the task ( relative to the root_dir ).
        """
        path_ = self.task_dir / self.dirnames.tmp
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def log_dir(self) -> Path:
        """
        Get the path to the log directory.

        Returns:
            path to the log directory of the task ( relative to the root_dir ).
        """
        path_ = self.task_dir / self.dirnames.logs
        path_.mkdir(parents=True, exist_ok=True)
        return path_

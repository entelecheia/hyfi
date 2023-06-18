from pathlib import Path
from typing import Any

from pydantic import BaseModel

from hyfi.hydra import Composer
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


class TaskPathConfig(BaseModel):
    config_name: str = "__task__"

    task_root: str = "tmp/task"
    task_outputs: str = ""
    task_datasets: str = ""
    task_library: str = ""
    task_models: str = ""
    task_cache: str = ""
    task_tmp: str = ""
    task_log: str = ""

    class Config:
        extra = "ignore"

    def __init__(
        self,
        config_name: str = "__task__",
        config_group: str = "path",
        **data: Any,
    ):
        """
        Initialize the batch. This is the method you call when you want to initialize the batch from a config

        Args:
                config_name: The name of the config you want to use
                data: The data you want to initilize the
        """
        super().__init__(**data)
        self.initialize_configs(
            config_name=config_name,
            config_group=config_group,
            **data,
        )

    def initialize_configs(
        self,
        config_name: str = "__task__",
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
    def root_dir(self) -> Path:
        """
        Returns the absolute path to the task root directory.

        Returns:
                an absolute path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        # return as an absolute path
        return Path(self.task_root).absolute()

    @property
    def output_dir(self) -> Path:
        """
        Returns the directory where the task outputs are stored. It is used to determine where the output files will be stored when running the task.


        Returns:
                absolute path to the output directory of the task ( relative to the task root directory ) or None if not
        """
        self.task_outputs = self.task_outputs or (self.root_dir / "outputs").as_posix()
        return Path(self.task_outputs).absolute()

    @property
    def library_dir(self) -> Path:
        """
        The path to the library.


        Returns:
                absolute path to the library directory ( relative to the task root directory ).
        """
        self.task_library = self.task_library or (self.root_dir / "library").as_posix()
        return Path(self.task_library).absolute()

    @property
    def dataset_dir(self) -> Path:
        """
        Get the path to the dataset directory.


        Returns:
                absolute path to the dataset directory ( relative to the root directory ) or None if not set in the
        """
        self.task_datasets = (
            self.task_datasets or (self.root_dir / "datasets").as_posix()
        )
        return Path(self.task_datasets).absolute()

    @property
    def model_dir(self) -> Path:
        """
        Get the directory where models are stored.


        Returns:
                Absolute path to the models directory on the task's filesystem ( relative to the root_dir )
        """
        self.task_models = self.task_models or (self.root_dir / "models").as_posix()
        return Path(self.task_models).absolute()

    @property
    def cache_dir(self) -> Path:
        """
        The directory where tasks are cached.


        Returns:
                A path to the cache directory for this task or None if it is not set in the config
        """
        self.task_cache = self.task_cache or (self.root_dir / "cache").as_posix()
        return Path(self.task_cache).absolute()

    @property
    def tmp_dir(self) -> Path:
        """
        Returns the path to the temporary directory.


        Returns:
                absolute path to the temporary directory of the task ( relative to the root_dir ).
        """
        self.task_tmp = self.task_tmp or (self.root_dir / "tmp").as_posix()
        return Path(self.task_tmp).absolute()

    @property
    def log_dir(self) -> Path:
        """
        Get the path to the log directory.


        Returns:
                absolute path to the log directory of the task ( relative to the root_dir ).
        """
        self.task_log = self.task_log or (self.root_dir / "logs").as_posix()
        log_dir = Path(self.task_log).absolute()
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

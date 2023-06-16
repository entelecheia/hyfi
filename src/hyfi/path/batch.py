from pathlib import Path
from typing import Any

from pydantic import BaseModel

from hyfi.hydra import _compose
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


class BatchPathConfig(BaseModel):
    config_name: str = "__batch__"

    project_workspace_root = ""
    batch_name: str = "demo"
    batch_output: str = ""
    task_name: str = "default-task"
    task_root: str = ""
    task_outputs: str = ""
    task_datasets: str = ""
    task_library: str = ""
    task_models: str = ""
    task_cache: str = ""
    task_tmp: str = ""
    task_log: str = ""

    class Config:
        extra = "ignore"

    def __init__(self, config_name: str = "__batch__", **data: Any):
        """
        Initialize the batch. This is the method you call when you want to initialize the batch from a config

        Args:
                config_name: The name of the config you want to use
                data: The data you want to initilize the
        """
        # Initialize the config with the given config_name.
        if not data:
            logger.debug(
                "There are no arguments to initilize a config, using default config %s",
                config_name,
            )
            data = _compose(f"path={config_name}")
        super().__init__(**data)

    @property
    def project_workspace_dir(self) -> Path:
        """
        Get the path to the project workspace directory.


        Returns:
                absolute path to the project workspace directory or None if not set by the user ( in which case a default is used )
        """
        self.project_workspace_root = self.project_workspace_root or "./workspace"
        return Path(self.project_workspace_root).absolute()

    @property
    def root_dir(self) -> Path:
        """
        Returns the absolute path to the task root directory. If the task_root attribute is set it is used as the path to the task's data directory. Otherwise the task name is used as the path to the project's data directory.


        Returns:
                an absolute path to the task root directory or None if it doesn't exist or cannot be converted to a path object
        """
        self.task_root = (
            self.task_root or (self.project_workspace_dir / self.task_name).as_posix()
        )
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
    def batch_dir(self) -> Path:
        """
        The directory where the batch is stored. It is used to determine where the results are stored for a batch of data to be processed.


        Returns:
                The directory where the batch output is stored for a batch of data to be processed ( relative to the task output directory )
        """
        self.batch_output = (
            self.batch_output or (self.output_dir / self.batch_name).as_posix()
        )
        return Path(self.batch_output).absolute()

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

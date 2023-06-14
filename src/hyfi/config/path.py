from pathlib import Path
from typing import Any

from pydantic import BaseModel

from hyfi.env import getLogger
from hyfi.hydra import _compose

logger = getLogger(__name__)


class PathConfig(BaseModel):
    config_name: str = "__batch__"

    project_data_root = ""
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
        if not data:
            logger.debug(
                "There are no arguments to initilize a config, using default config %s",
                config_name,
            )
            data = _compose(f"path={config_name}")
        super().__init__(**data)

    @property
    def project_data_dir(self):
        self.project_data_root = self.project_data_root or "./workspace"
        return Path(self.project_data_root).absolute()

    @property
    def root_dir(self):
        self.task_root = (
            self.task_root or (self.project_data_dir / self.task_name).as_posix()
        )
        # return as an absolute path
        return Path(self.task_root).absolute()

    @property
    def output_dir(self):
        self.task_outputs = self.task_outputs or (self.root_dir / "outputs").as_posix()
        return Path(self.task_outputs).absolute()

    @property
    def batch_dir(self):
        self.batch_output = (
            self.batch_output or (self.output_dir / self.batch_name).as_posix()
        )
        return Path(self.batch_output).absolute()

    @property
    def library_dir(self):
        self.task_library = self.task_library or (self.root_dir / "library").as_posix()
        return Path(self.task_library).absolute()

    @property
    def dataset_dir(self):
        self.task_datasets = (
            self.task_datasets or (self.root_dir / "datasets").as_posix()
        )
        return Path(self.task_datasets).absolute()

    @property
    def model_dir(self):
        self.task_models = self.task_models or (self.root_dir / "models").as_posix()
        return Path(self.task_models).absolute()

    @property
    def cache_dir(self):
        self.task_cache = self.task_cache or (self.root_dir / "cache").as_posix()
        return Path(self.task_cache).absolute()

    @property
    def tmp_dir(self):
        self.task_tmp = self.task_tmp or (self.root_dir / "tmp").as_posix()
        return Path(self.task_tmp).absolute()

    @property
    def log_dir(self):
        self.task_log = self.task_log or (self.root_dir / "logs").as_posix()
        log_dir = Path(self.task_log).absolute()
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

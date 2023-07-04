from pathlib import Path

from pydantic import BaseModel

from hyfi.path.dirnames import DirnamesConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BasePathConfig(BaseModel):
    _name_: str = "base"
    dirnames: DirnamesConfig = DirnamesConfig()

    @property
    def name(self) -> str:
        """
        Returns the name of the path configuration.
        """
        return self._name_

    @property
    def root_dir(self) -> Path:
        """
        Returns the path to the root directory.
        """
        # return as an path
        path_ = Path(".")
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def workspace_dir(self) -> Path:
        """
        Returns the path to the workspace directory.
        """
        path_ = self.root_dir / "workspace"
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def input_dir(self) -> Path:
        """
        Returns the directory where the inputs are stored.
        """
        path_ = self.workspace_dir / self.dirnames.inputs
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def output_dir(self) -> Path:
        """
        Returns the directory where the outputs are stored.
        """
        path_ = self.workspace_dir / self.dirnames.outputs
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def dataset_dir(self) -> Path:
        """
        Get the path to the dataset directory.
        """
        path_ = self.workspace_dir / self.dirnames.datasets
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def model_dir(self) -> Path:
        """
        Get the directory where models are stored.
        """
        path_ = self.workspace_dir / self.dirnames.models
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def module_dir(self) -> Path:
        """
        Create and return the path to the module directory.
        """
        path_ = self.workspace_dir / self.dirnames.modules
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def library_dir(self) -> Path:
        """
        Create and return the path to the library directory.
        """
        path_ = self.workspace_dir / self.dirnames.library
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def log_dir(self):
        """
        Create and return the path to the log directory.
        """
        path_ = self.workspace_dir / self.dirnames.logs
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def cache_dir(self):
        """
        Create and return the directory where cache files are stored.
        """
        path_ = self.workspace_dir / self.dirnames.cache
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def tmp_dir(self):
        """
        Create and return the directory where temporary files are stored.
        """
        path_ = self.workspace_dir / self.dirnames.tmp
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def config_dir(self):
        """
        Directory for the configuration files.
        """
        config_dir = self.workspace_dir / self.dirnames.config_dirname
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    @property
    def config_filename(self):
        """
        Name of the YAML configuration file.
        """
        return f"{self.name}_{self.dirnames.config_yaml}"

    @property
    def config_jsonfile(self):
        """
        Name of the JSON configuration file.
        """
        return f"{self.name}_{self.dirnames.config_json}"

    @property
    def config_filepath(self):
        """
        Path to the YAML configuration file.
        """
        return self.config_dir / self.config_filename

    @property
    def config_jsonpath(self):
        """
        Path to the JSON configuration file.
        """
        return self.config_dir / self.config_jsonfile

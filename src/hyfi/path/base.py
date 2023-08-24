from pathlib import Path
from typing import Optional, Union

from hyfi.composer import BaseConfig
from hyfi.path.dirnames import Dirnames
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BasePath(BaseConfig):
    _config_name_: str = "__init__"
    _config_group_: str = "/path"

    dirnames: Dirnames = Dirnames()

    @property
    def name(self) -> str:
        """
        Returns the name of the path configuration.
        """
        return self._config_name_

    @property
    def root_dir(self) -> Path:
        """
        Returns the path to the root directory.
        """
        return Path(".").absolute()

    @property
    def workspace_dir(self) -> Path:
        """
        Returns the path to the workspace directory.
        """
        return self.root_dir / "workspace"

    def get_path(
        self,
        path_name: str,
        base_dir: Optional[Union[Path, str]] = None,
        ensure_exists: bool = False,
    ) -> Path:
        """
        Get the path to a directory or file.
        """
        if not hasattr(self.dirnames, path_name):
            raise AttributeError(f"Path '{path_name}' does not exist.")
        base_dir = base_dir or self.workspace_dir
        path_ = Path(base_dir) / getattr(self.dirnames, path_name)
        if ensure_exists:
            path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def archive_dir(self) -> Path:
        """
        Returns the directory where the archives are stored.
        """
        return self.get_path("archives")

    @property
    def input_dir(self) -> Path:
        """
        Returns the directory where the inputs are stored.
        """
        return self.get_path("inputs")

    @property
    def output_dir(self) -> Path:
        """
        Returns the directory where the outputs are stored.
        """
        return self.get_path("outputs")

    @property
    def dataset_dir(self) -> Path:
        """
        Get the path to the dataset directory.
        """
        return self.get_path("datasets")

    @property
    def model_dir(self) -> Path:
        """
        Get the directory where models are stored.
        """
        return self.get_path("models")

    @property
    def module_dir(self) -> Path:
        """
        Create and return the path to the module directory.
        """
        return self.get_path("modules")

    @property
    def library_dir(self) -> Path:
        """
        Create and return the path to the library directory.
        """
        return self.get_path("library")

    @property
    def log_dir(self):
        """
        Create and return the path to the log directory.
        """
        return self.get_path("logs")

    @property
    def cache_dir(self):
        """
        Create and return the directory where cache files are stored.
        """
        return self.get_path("cache")

    @property
    def tmp_dir(self):
        """
        Create and return the directory where temporary files are stored.
        """
        return self.get_path("tmp")

    @property
    def config_dir(self):
        """
        Directory for the configuration files.
        """
        return self.get_path("configs")

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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"

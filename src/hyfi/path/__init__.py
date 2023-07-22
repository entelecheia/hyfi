from pathlib import Path

from hyfi.composer.base import BaseConfig
from hyfi.path.base import BasePathConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class PathConfig(BaseConfig, BasePathConfig):
    _config_name_: str = "__init__"
    _config_group_: str = "path"

    # internal paths for hyfi
    home: str = ""
    hyfi: str = ""
    resources: str = ""
    runtime: str = ""
    # global paths
    global_hyfi_root: str = ""
    global_workspace_name: str = ".hyfi"
    # project specific paths
    project_name: str = ""
    project_root: str = ""
    project_workspace_name: str = "workspace"

    @property
    def global_root_dir(self) -> Path:
        """
        Create and return the path to the hyfi directory.

        Returns:
            path to the hyfi directory
        """
        path_ = Path(self.global_hyfi_root)
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def global_workspace_dir(self) -> Path:
        """
        Create and return the path to the glboal workspace directory.

        Returns:
            path to the global workspace directory
        """
        path_ = self.global_root_dir / self.global_workspace_name
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def global_archive_dir(self) -> Path:
        """
        Create and return the path to the global archive directory.

        Returns:
            path to the global archive directory
        """
        return self.get_path("archives", self.global_workspace_dir)

    @property
    def glboal_dataset_dir(self) -> Path:
        """
        Create and return the path to the global datasets directory.

        Returns:
            path to the global datasets directory
        """
        return self.get_path("datasets", self.global_workspace_dir)

    @property
    def global_model_dir(self) -> Path:
        """
        Create and return the path to the global models directory.

        Returns:
            path to the global models directory
        """
        return self.get_path("models", self.global_workspace_dir)

    @property
    def glboal_module_dir(self) -> Path:
        """
        Create and return the path to the global modules directory.

        Returns:
            path to the global modules directory
        """
        return self.get_path("modules", self.global_workspace_dir)

    @property
    def global_library_dir(self) -> Path:
        """
        Create and return the path to the global library directory.

        Returns:
            path to the global library directory
        """
        return self.get_path("library", self.global_workspace_dir)

    @property
    def glboal_log_dir(self) -> Path:
        """
        Create and return the path to the global log directory.

        Returns:
            path to the global log directory
        """
        return self.get_path("logs", self.global_workspace_dir)

    @property
    def global_cache_dir(self) -> Path:
        """
        Create and return the path to the global cache directory.

        Returns:
            path to the global cache directory
        """
        return self.get_path("cache", self.global_workspace_dir)

    @property
    def global_tmp_dir(self) -> Path:
        """
        Create and return the path to the global tmp directory.

        Returns:
            path to the global tmp directory
        """
        return self.get_path("tmp", self.global_workspace_dir)

    @property
    def name(self) -> str:
        """
        Returns the name of the path configuration.
        """
        return self.project_name

    @property
    def root_dir(self) -> Path:
        """
        Create and return the path to the project directory.

        Returns:
            path to the project directory
        """
        path_ = Path(self.project_root)
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def workspace_dir(self) -> Path:
        """
        Create and return the path to the project workspace directory.

        Returns:
            path to the project workspace directory
        """
        path_ = self.root_dir / self.project_workspace_name
        path_.mkdir(parents=True, exist_ok=True)
        return path_

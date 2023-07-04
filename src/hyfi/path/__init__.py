from pathlib import Path

from hyfi.__global__ import __about__
from hyfi.composer import BaseConfig
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
    global_workspace_name: str = "workspace"
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
        path_ = self.global_workspace_dir / self.dirnames.archive
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def glboal_dataset_dir(self) -> Path:
        """
        Create and return the path to the global datasets directory.

        Returns:
            path to the global datasets directory
        """
        path_ = self.global_workspace_dir / self.dirnames.datasets
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def global_model_dir(self) -> Path:
        """
        Create and return the path to the global models directory.

        Returns:
            path to the global models directory
        """
        path_ = self.global_workspace_dir / self.dirnames.models
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def glboal_module_dir(self) -> Path:
        """
        Create and return the path to the global modules directory.

        Returns:
            path to the global modules directory
        """
        path_ = self.global_workspace_dir / self.dirnames.modules
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def global_library_dir(self) -> Path:
        """
        Create and return the path to the global library directory.

        Returns:
            path to the global library directory
        """
        path_ = self.global_workspace_dir / self.dirnames.library
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def glboal_log_dir(self) -> Path:
        """
        Create and return the path to the global log directory.

        Returns:
            path to the global log directory
        """
        path_ = self.global_workspace_dir / self.dirnames.logs
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def global_cache_dir(self) -> Path:
        """
        Create and return the path to the global cache directory.

        Returns:
            path to the global cache directory
        """
        path_ = self.global_workspace_dir / self.dirnames.cache
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def global_tmp_dir(self) -> Path:
        """
        Create and return the path to the global tmp directory.

        Returns:
            path to the global tmp directory
        """
        path_ = self.global_workspace_dir / self.dirnames.tmp
        path_.mkdir(parents=True, exist_ok=True)
        return path_

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

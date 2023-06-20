from pathlib import Path
from typing import Any

from pydantic import BaseModel

from hyfi.__global__ import __about__
from hyfi.composer import BaseConfig
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


class PathConfig(BaseConfig):
    config_name: str = "__init__"
    config_group: str = "path"

    # internal paths for hyfi
    home: str = ""
    hyfi: str = ""
    resources: str = ""
    runtime: str = ""
    # global paths
    global_hyfi_root: str = ""
    global_workspace_name: str = "workspace"
    global_workspace_root: str = ""
    global_archive: str = ""
    global_datasets: str = ""
    global_models: str = ""
    global_modules: str = ""
    global_library: str = ""
    global_cache: str = ""
    global_tmp: str = ""
    # project specific paths
    project_root: str = ""
    project_workspace_name: str = "workspace"
    project_workspace_root: str = ""
    project_archive: str = ""
    project_datasets: str = ""
    project_models: str = ""
    project_modules: str = ""
    project_outputs: str = ""
    project_logs: str = ""
    project_library: str = ""
    project_cache: str = ""
    project_tmp: str = ""

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    def initialize_configs(self, **config_kwargs):
        # Initialize the config with the given config_name.
        super().initialize_configs(**config_kwargs)

    @property
    def log_dir(self):
        """
        Create and return the path to the log directory. This is a convenience method for use in unit tests that want to ensure that the log directory exists and is accessible to the user.


        Returns:
                absolute path to the log directory for the project ( including parent directories
        """
        Path(self.project_logs).mkdir(parents=True, exist_ok=True)
        return Path(self.project_logs).absolute()

    @property
    def cache_dir(self):
        """
        Create and return the directory where cache files are stored. This is useful for debugging and to ensure that we don't accidentally delete the cache files when there are too many files in the cache.


        Returns:
                absolute path to the cache directory for this test run
        """
        Path(self.global_cache).mkdir(parents=True, exist_ok=True)
        return Path(self.global_cache).absolute()

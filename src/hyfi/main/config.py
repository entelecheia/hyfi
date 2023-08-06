"""
Hyfi configuration file.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

from omegaconf import DictConfig

from hyfi.about import AboutConfig
from hyfi.composer import (
    BaseModel,
    ConfigDict,
    FieldValidationInfo,
    PrivateAttr,
    field_validator,
    model_validator,
)
from hyfi.core import global_hyfi
from hyfi.dotenv import DotEnvConfig
from hyfi.project import ProjectConfig
from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING
from hyfi.utils.notebooks import NBs

logger = LOGGING.getLogger(__name__)

ConfigType = Union[DictConfig, Dict]

__default_project_root__ = "."
__default_workspace_name__ = "workspace"


class GlobalConfig(BaseModel):
    """HyFI global config class.  This class is used to store the configuration"""

    debug_mode: bool = False
    noop: bool = False
    dryrun: bool = False
    resolve: bool = False
    verbose: bool = False
    logging_level: str = "WARNING"

    hydra: Optional[ConfigType] = None

    about: Optional[AboutConfig] = None
    copier: Optional[ConfigType] = None
    project: Optional[ProjectConfig] = None
    pipeline: Optional[ConfigType] = None
    task: Optional[ConfigType] = None
    workflow: Optional[ConfigType] = None
    tasks: Optional[List[str]] = None

    _version_: str = PrivateAttr(global_hyfi.version)
    _initilized_: bool = PrivateAttr(False)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="allow",
    )  # type: ignore

    @model_validator(mode="before")
    def _validate_model_data(cls, data):
        """
        Validate and set the model data.

        Args:
            cls: Class to use for config lookup
            data: Dictionary of values to check and set

        Returns:
            Validated dictionary of values
        """
        key = "hyfi_config_path"
        val = ENVs.check_and_set_osenv_var(key, data.get(key))
        # Set the hyfi_config_module value in the configuration file.
        if val is not None:
            data[key] = val
            key = "hyfi_config_module"
            data[key] = ENVs.check_and_set_osenv_var(key, val.replace("pkg://", ""))
        return data

    @field_validator("logging_level")
    def _validate_logging_level(cls, v, info: FieldValidationInfo):
        """
        Validate and set the logging level
        """
        verbose = info.data.get("verbose", False)
        # Set verbose to INFO.
        if verbose and v == "WARNING":
            v = "INFO"
        logger.setLevel(v)
        return v

    def init_project(
        self,
        project_name: Optional[str] = None,
        project_description: Optional[str] = None,
        project_root: Optional[str] = None,
        project_workspace_name: Optional[str] = None,
        global_hyfi_root: Optional[str] = None,
        global_workspace_name: Optional[str] = None,
        num_workers: Optional[int] = None,
        log_level: Optional[str] = None,
        reinit: bool = True,
        autotime: bool = True,
        retina: bool = True,
        verbose: Union[bool, int] = False,
        **project_kwargs,
    ):
        """
        Initialize and start hyfi.

        Args:
            project_name: Name of the project to use.
            project_description: Description of the project that will be used.
            project_root: Root directory of the project.
            project_workspace_name: Name of the project's workspace directory.
            global_hyfi_root: Root directory of the global hyfi.
            global_workspace_name: Name of the global hierachical workspace directory.
            num_workers: Number of workers to run.
            log_level: Log level for the log.
            autotime: Whether to automatically set time and / or keep track of run times.
            retina: Whether to use retina or not.
            verbose: Enables or disables logging
        """
        if self._initilized_ and not reinit:
            return
        if self.about is None:
            self.about = AboutConfig()
        # ENVs.load_dotenv()
        envs = DotEnvConfig(HYFI_VERBOSE=verbose)  # type: ignore
        # Set the project name environment variable HYFI_PROJECT_NAME environment variable if project_name is not set.
        if project_name:
            envs.HYFI_PROJECT_NAME = ENVs.expand_posix_vars(project_name)
        # Set the project description environment variable HYFI_PROJECT_DESC environment variable.
        if project_description:
            envs.HYFI_PROJECT_DESC = ENVs.expand_posix_vars(project_description)
        # Set environment variables HYFI_PROJECT_ROOT to the project root if project_root is set to true.
        if project_root:
            envs.HYFI_PROJECT_ROOT = ENVs.expand_posix_vars(project_root)
        # Set the project workspace name environment variable HYFI_PROJECT_WORKSPACE_NAME environment variable if project_workspace_name is set to the project workspace name.
        if project_workspace_name:
            envs.HYFI_PROJECT_WORKSPACE_NAME = ENVs.expand_posix_vars(
                project_workspace_name
            )
        # Expand the hyfi_root environment variable.
        if global_hyfi_root:
            envs.HYFI_GLOBAL_ROOT = ENVs.expand_posix_vars(global_hyfi_root)
        # Set the global workspace name environment variable HYFI_GLOBAL_WORKSPACE_NAME environment variable.
        if global_workspace_name:
            envs.HYFI_GLOBAL_WORKSPACE_NAME = ENVs.expand_posix_vars(
                global_workspace_name
            )
        # Set the number of workers to use.
        if num_workers:
            envs.HYFI_NUM_WORKERS = num_workers
        # Set the log level to the given log level.
        if log_level:
            envs.HYFI_LOG_LEVEL = log_level
            LOGGING.setLogger(log_level)
            logger.setLevel(log_level)
        # Load the extentions for the autotime extension.
        if autotime:
            NBs.load_extentions(exts=["autotime"])
        # Set the retina matplotlib formats.
        if retina:
            NBs.set_matplotlib_formats("retina")

        self.project = ProjectConfig(**project_kwargs)
        logger.info("HyFi project [%s] initialized", self.project.project_name)
        self._initilized_ = True

    def terminate(self) -> None:
        """
        Terminate hyfi config by stopping joblib

        Returns:
            True if successful False
        """
        # If the module is not initialized yet.
        if not self._initilized_:
            return
        # Stop the backend if the joblib is running.
        if self.project and self.project.joblib:
            self.project.joblib.stop_backend()
        self._initilized_ = False

    def __repr__(self):
        """
        Returns a string representation of HyFIConfig.

        Returns:
            The string representation of HyFI
        """
        return f"HyFIConfig(project={self.project})"

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
                The string representation of the
        """
        return self.__repr__()

    @property
    def app_version(self):
        """
        Get the version of the application.


        Returns:
            The version of the application
        """
        return global_hyfi.version

    @property
    def app_name(self):
        """
        Get the name of the application.

        Returns:
            The name of the application
        """
        return self.about.name if self.about else global_hyfi.hyfi_name

    @property
    def package_name(self):
        """
        Get the name of the package.

        Returns:
            The name of the package
        """
        return global_hyfi.package_name

    @property
    def dotenv(self):
        return DotEnvConfig()  # type: ignore

    @property
    def osenv(self):
        return os.environ

    def print_about(self, **kwargs):
        self.about = AboutConfig(**kwargs)
        pkg_name = self.package_name
        name = self.app_name
        print()
        for k, v in self.about.model_dump().items():
            if k.startswith("_") or k == "version":
                continue
            print(f"{k:11} : {v}")
        print(f"{'version':11} : {self.app_version}")
        if pkg_name:
            print(f"\nExecute `{pkg_name} --help` to see what you can do with {name}")

    @property
    def project_dir(self) -> Path:
        """Get the project root directory."""
        return (
            self.project.root_dir
            if self.project
            else Path(__default_project_root__).absolute()
        )

    @property
    def project_workspace_dir(self) -> Path:
        """Get the project workspace directory."""
        return (
            self.project.workspace_dir
            if self.project
            else self.project_dir / __default_workspace_name__
        )

    def get_path(
        self,
        path_name: str,
        base_dir: Optional[Union[Path, str]] = None,
    ) -> Optional[Path]:
        """
        Get the path to a directory or file.
        """
        return (
            self.project.get_path(path_name, base_dir=base_dir)
            if self.project
            else None
        )


global_config = GlobalConfig()


def __project_root_path__() -> str:
    """Global HyFI config path for the project root."""
    return str(global_config.project_dir or "")


def __project_workspace_path__() -> str:
    """Global HyFI config path for the project workspace directory."""
    return str(global_config.project_workspace_dir or "")


def __get_path__(path_name: str, base_dir: Optional[str] = None) -> str:
    """
    Get the path to a directory or file.
    """
    return str(global_config.get_path(path_name, base_dir=base_dir) or "")

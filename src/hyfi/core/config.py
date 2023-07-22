"""
Hyfi configuration file.
"""
import os
from typing import Any, List, Optional, Union

from omegaconf import DictConfig
from pydantic import (
    BaseModel,
    ConfigDict,
    FieldValidationInfo,
    PrivateAttr,
    field_validator,
    model_validator,
)

from hyfi.about import AboutConfig, __app_name__
from hyfi.core import __about__, __app_version__, __hydra_config__
from hyfi.dotenv import DotEnvConfig
from hyfi.pipeline import PipelineConfig
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING
from hyfi.utils.notebooks import NBs
from hyfi.workflow import WorkflowConfig

logger = LOGGING.getLogger(__name__)


class HyfiConfig(BaseModel):
    """HyFI root config class.  This class is used to store the configuration"""

    hyfi_config_path: str = __about__.config_path
    hyfi_config_module: str = __about__.config_module
    hyfi_user_config_path: str = __about__.user_config_path

    debug_mode: bool = False
    resolve: bool = False
    verbose: bool = False
    logging_level: str = "WARNING"

    hydra: Optional[DictConfig] = None

    about: Optional[AboutConfig] = None
    copier: Optional[DictConfig] = None
    project: Optional[ProjectConfig] = None
    pipeline: Optional[PipelineConfig] = None
    task: Optional[TaskConfig] = None
    workflow: Optional[WorkflowConfig] = None
    tasks: Optional[List[str]] = None

    _version_: str = PrivateAttr(__app_version__())
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

    @field_validator("hyfi_user_config_path")
    def _validate_hyfi_user_config_path(cls, v):
        """
        Validate and set hyfi_user_config_path.

        Args:
            cls: Class to use for validation.
            v: Value to set if valid.

        Returns:
            True if valid False otherwise
        """
        return ENVs.check_and_set_osenv_var("hyfi_user_config_path", v)

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

    def __init__(self, **config_kwargs: Any):
        """
        Initialize the object with data

        Args:
            config_kwargs: Dictionary of values to initialize the object with
        """
        super().__init__(**config_kwargs)

    def init_project(
        self,
        project_name: str = "",
        project_description: str = "",
        project_root: str = "",
        project_workspace_name: str = "",
        global_hyfi_root: str = "",
        global_workspace_name: str = "",
        num_workers: int = -1,
        log_level: str = "",
        reinit: bool = True,
        autotime: bool = True,
        retina: bool = True,
        verbose: Union[bool, int] = False,
        **kwargs,
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

        self.initialize(force=reinit)
        self.project = ProjectConfig()

    def initialize(self, force: bool = False) -> None:
        """
        Initialize hyfi.

        Returns:
            A boolean indicating whether initialization was successful
        """
        # Returns the current value of the _initilized_ attribute.
        if self._initilized_ and not force:
            return
        if self.about is None:
            self.about = AboutConfig()
        __hydra_config__.hyfi_config_module = __about__.config_module
        __hydra_config__.hyfi_config_path = __about__.config_path
        __hydra_config__.hyfi_user_config_path = self.hyfi_user_config_path
        logger.debug(
            "HyFiConfig initialized with hyfi_config_module=%s, hyfi_config_path=%s, hyfi_user_config_path=%s",
            __hydra_config__.hyfi_config_module,
            __hydra_config__.hyfi_config_path,
            __hydra_config__.hyfi_user_config_path,
        )
        ENVs.load_dotenv()

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
        return __app_version__()

    @property
    def app_name(self):
        """
        Get the name of the application.

        Returns:
            The name of the application
        """
        return self.about.name if self.about else __app_name__

    @property
    def dotenv(self):
        return DotEnvConfig()  # type: ignore

    @property
    def osenv(self):
        return os.environ

    def print_about(self, **kwargs):
        about = AboutConfig(**kwargs)
        pkg_name = kwargs.get("__package_name__", about.__package_name__)
        name = about.name
        print()
        for k, v in about.model_dump().items():
            if k.startswith("_") or k == "version":
                continue
            print(f"{k:11} : {v}")
        print(f"{'version':11} : {self.app_version}")
        if pkg_name:
            print(f"\nExecute `{pkg_name} --help` to see what you can do with {name}")

    def get_project_path(self, path_name: str) -> str:
        if self.project and self.project.path:
            return str(self.project.path.get_path(path_name))
        return ""


__global_config__ = HyfiConfig()


def __search_package_path__():
    """Global HyFI config path for the package to search for."""
    return __global_config__.hyfi_config_path

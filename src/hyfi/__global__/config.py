"""
Hyfi configuration file.
"""
from typing import Any, Dict, Optional, Union

from omegaconf import DictConfig
from pydantic import BaseModel, root_validator, validator

from hyfi.__global__ import __about__, __hydra_config__
from hyfi.about import AboutConfig
from hyfi.dotenv import DotEnvConfig
from hyfi.hydra import _compose
from hyfi.project import ProjectConfig
from hyfi.utils.env import _check_and_set_value, expand_posix_vars
from hyfi.utils.logging import getLogger, setLogger
from hyfi.utils.notebook import load_extentions, set_matplotlib_formats

logger = getLogger(__name__)


def __version__():
    """
    Returns the version of Hyfi. It is used to determine the version of Hyfi.


    Returns:
        string containing the version of
    """
    from hyfi._version import __version__

    return __version__


class HyfiConfig(BaseModel):
    """HyFI config primary class"""

    hyfi_config_path: str = __about__.config_path
    hyfi_config_module: str = __about__.config_module
    hyfi_user_config_path: str = ""

    debug_mode: bool = False
    print_config: bool = False
    print_resolved_config: bool = False
    verbose: bool = False
    logging_level: str = "WARNING"

    hydra: Optional[DictConfig] = None

    about: AboutConfig = AboutConfig()
    project: Optional[ProjectConfig] = None
    copier: Optional[DictConfig] = None

    __version__: str = __version__()
    __initilized__: bool = False

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
        validate_assignment = True
        extra = "allow"

    @root_validator()
    def _check_and_set_values(cls, values):
        """
        Validate and set values for the config file.

        Args:
                cls: Class to use for config lookup
                values: Dictionary of values to check and set

        Returns:
                Same dictionary with hyfi_config
        """
        key = "hyfi_config_path"
        val = _check_and_set_value(key, values.get(key))
        values[key] = val
        # Set the hyfi_config_module value in the configuration file.
        if val is not None:
            key = "hyfi_config_module"
            values[key] = _check_and_set_value(key, val.replace("pkg://", ""))
        return values

    @validator("hyfi_user_config_path")
    def _validate_hyfi_user_config_path(cls, v):
        """
        Validate and set hyfi_user_config_path.

        Args:
                cls: Class to use for validation.
                v: Value to set if valid.

        Returns:
                True if valid False otherwise
        """
        return _check_and_set_value("hyfi_user_config_path", v)

    @validator("logging_level")
    def _validate_logging_level(cls, v, values):
        """
        Validate and set the logging level

        Args:
                cls: The class to operate on
                v: The value to set the logging level to
                values: The values from the config file

        Returns:
                The value that was set
        """
        verbose = values.get("verbose", False)
        # Set verbose to INFO.
        if verbose and v == "WARNING":
            v = "INFO"
        logger.setLevel(v)
        return v

    def __init__(self, **data: Any):
        """
        Initialize the object with data

        Args:
                data: Data to initialize the
        """
        super().__init__(**data)
        # self.about = __about__

    def init_workspace(
        self,
        project_name: str = "",
        task_name: str = "",
        project_description: str = "",
        project_root: str = "",
        project_workspace_name: str = "",
        global_hyfi_root: str = "",
        global_workspace_name: str = "",
        num_workers: int = -1,
        log_level: str = "",
        autotime: bool = True,
        retina: bool = True,
        verbose: Union[bool, int] = False,
        **kwargs,
    ):
        """
        Initialize and start hyfi.

        Args:
                project_name: Name of the project to use.
                task_name: Name of the task to use.
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
        envs = DotEnvConfig(HYFI_VERBOSE=verbose)
        # Set the project name environment variable HYFI_PROJECT_NAME environment variable if project_name is not set.
        if project_name:
            envs.HYFI_PROJECT_NAME = expand_posix_vars(project_name)
        # Set the task name environment variable HYFI_TASK_NAME to the task name.
        if task_name:
            envs.HYFI_TASK_NAME = expand_posix_vars(task_name)
        # Set the project description environment variable HYFI_PROJECT_DESC environment variable.
        if project_description:
            envs.HYFI_PROJECT_DESC = expand_posix_vars(project_description)
        # Set environment variables HYFI_PROJECT_ROOT to the project root if project_root is set to true.
        if project_root:
            envs.HYFI_PROJECT_ROOT = expand_posix_vars(project_root)
        # Set the project workspace name environment variable HYFI_PROJECT_WORKSPACE_NAME environment variable if project_workspace_name is set to the project workspace name.
        if project_workspace_name:
            envs.HYFI_PROJECT_WORKSPACE_NAME = expand_posix_vars(project_workspace_name)
        # Expand the hyfi_root environment variable.
        if global_hyfi_root:
            envs.HYFI_GLOBAL_ROOT = expand_posix_vars(global_hyfi_root)
        # Set the global workspace name environment variable HYFI_GLOBAL_WORKSPACE_NAME environment variable.
        if global_workspace_name:
            envs.HYFI_GLOBAL_WORKSPACE_NAME = expand_posix_vars(global_workspace_name)
        # Set the number of workers to use.
        if num_workers:
            envs.HYFI_NUM_WORKERS = num_workers
        # Set the log level to the given log level.
        if log_level:
            envs.HYFI_LOG_LEVEL = log_level
            setLogger(log_level)
            logger.setLevel(log_level)
        # Load the extentions for the autotime extension.
        if autotime:
            load_extentions(exts=["autotime"])
        # Set the retina matplotlib formats.
        if retina:
            set_matplotlib_formats("retina")
        self.initialize()

    def initialize(self, config: Union[DictConfig, Dict, None] = None):
        """
        Initialize hyfi. This is called by : meth : ` __init__ ` to perform initialisation.

        Args:
                config: Configuration dictionary or None.

        Returns:
                A boolean indicating whether initialization was successful
        """
        """Initialize hyfi config"""
        # Returns the current value of the __initilized__ attribute.
        if self.__initilized__:
            return
        __hydra_config__.hyfi_config_module = self.hyfi_config_module
        __hydra_config__.hyfi_config_path = self.hyfi_config_path
        __hydra_config__.hyfi_user_config_path = self.hyfi_user_config_path

        # If config is not set the default config is used.
        if config is None:
            config = _compose(
                overrides=["+project=__init__"], config_module=__about__.config_module
            )
            logger.debug("Using default config.")

        # Skip project config initialization.
        if "project" not in config:
            logger.warning(
                "No project config found, skip project config initialization."
            )
            return
        self.project = ProjectConfig(**config["project"])
        self.project.init_project()
        # Initialize joblib backend if joblib is not set.
        if self.project.joblib:
            self.project.joblib.init_backend()

        self.__initilized__ = True

    def terminate(self):
        """
        Terminate hyfi config by stopping joblib


        Returns:
                True if successful False
        """
        """Terminate hyfi config"""
        # If the module is not initialized yet.
        if not self.__initilized__:
            return
        # Stop the backend if the joblib is running.
        if self.project and self.project.joblib:
            self.project.joblib.stop_backend()
        self.__initilized__ = False

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
        return self.about.version


__global_config__ = HyfiConfig()

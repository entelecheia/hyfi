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
    """Returns the version of HyFI"""
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
        key = "hyfi_config_path"
        val = _check_and_set_value(key, values.get(key))
        values[key] = val
        if val is not None:
            key = "hyfi_config_module"
            values[key] = _check_and_set_value(key, val.replace("pkg://", ""))
        return values

    @validator("hyfi_user_config_path")
    def _validate_hyfi_user_config_path(cls, v):
        return _check_and_set_value("hyfi_user_config_path", v)

    @validator("logging_level")
    def _validate_logging_level(cls, v, values):
        verbose = values.get("verbose", False)
        if verbose and v == "WARNING":
            v = "INFO"
        logger.setLevel(v)
        return v

    def __init__(self, **data: Any):
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
        envs = DotEnvConfig(HYFI_VERBOSE=verbose)
        if project_name:
            envs.HYFI_PROJECT_NAME = expand_posix_vars(project_name)
        if task_name:
            envs.HYFI_TASK_NAME = expand_posix_vars(task_name)
        if project_description:
            envs.HYFI_PROJECT_DESC = expand_posix_vars(project_description)
        if project_root:
            envs.HYFI_PROJECT_ROOT = expand_posix_vars(project_root)
        if project_workspace_name:
            envs.HYFI_PROJECT_WORKSPACE_NAME = expand_posix_vars(project_workspace_name)
        if global_hyfi_root:
            envs.HYFI_GLOBAL_ROOT = expand_posix_vars(global_hyfi_root)
        if global_workspace_name:
            envs.HYFI_GLOBAL_WORKSPACE_NAME = expand_posix_vars(global_workspace_name)
        if num_workers:
            envs.HYFI_NUM_WORKERS = num_workers
        if log_level:
            envs.HYFI_LOG_LEVEL = log_level
            setLogger(log_level)
            logger.setLevel(log_level)
        if autotime:
            load_extentions(exts=["autotime"])
        if retina:
            set_matplotlib_formats("retina")
        self.initialize()

    def initialize(self, config: Union[DictConfig, Dict, None] = None):
        """Initialize hyfi config"""
        if self.__initilized__:
            return
        __hydra_config__.hyfi_config_module = self.hyfi_config_module
        __hydra_config__.hyfi_config_path = self.hyfi_config_path
        __hydra_config__.hyfi_user_config_path = self.hyfi_user_config_path

        if config is None:
            config = _compose(
                overrides=["+project=__init__"], config_module=__about__.config_module
            )
            logger.debug("Using default config.")

        if "project" not in config:
            logger.warning(
                "No project config found, skip project config initialization."
            )
            return
        self.project = ProjectConfig(**config["project"])
        self.project.init_project()
        if self.project.joblib:
            self.project.joblib.init_backend()

        self.__initilized__ = True

    def terminate(self):
        """Terminate hyfi config"""
        if not self.__initilized__:
            return
        if self.project and self.project.joblib:
            self.project.joblib.stop_backend()
        self.__initilized__ = False

    def __repr__(self):
        return f"HyFIConfig(project={self.project})"

    def __str__(self):
        return self.__repr__()

    @property
    def app_version(self):
        return self.about.version


__global_config__ = HyfiConfig()

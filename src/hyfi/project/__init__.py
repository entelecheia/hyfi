import os
from pathlib import Path
from typing import Union

from pydantic import validator

from hyfi.__global__ import __about__
from hyfi.composer import BaseConfig
from hyfi.dotenv import DotEnvConfig
from hyfi.joblib import JobLibConfig
from hyfi.path import PathConfig
from hyfi.utils.logging import Logging
from hyfi.utils.notebooks import NBs

logger = Logging.getLogger(__name__)


class ProjectConfig(BaseConfig):
    """Project Config"""

    config_name: str = "__init__"
    config_group: str = "project"
    # Project Config
    project_name: str = "hyfi-project"
    task_name: str = ""
    project_description: str = ""
    project_root: str = ""
    project_workspace_name: str = "workspace"
    global_hyfi_root: str = ""
    global_workspace_name: str = "workspace"
    num_workers: int = 1
    use_huggingface_hub: bool = False
    use_wandb: bool = False
    verbose: Union[bool, int] = False
    # Config Classes
    dotenv: DotEnvConfig = None  # type: ignore
    joblib: JobLibConfig = None  # type: ignore
    path: PathConfig = None  # type: ignore

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    @validator("project_name", allow_reuse=True)
    def _validate_project_name(cls, v):
        if v is None:
            raise ValueError("Project name must be specified.")
        return v

    @validator("verbose", allow_reuse=True)
    def _validate_verbose(cls, v):
        if isinstance(v, str):
            if v.lower() in {"true", "1"}:
                v = True
            elif v.lower() in {"false", "0"}:
                v = False
            else:
                raise ValueError("verbose must be a boolean or a string of 0 or 1")
        return v

    def initialize_configs(self, **config_kwargs):
        super().initialize_configs(**config_kwargs)

        self.dotenv = DotEnvConfig()
        self.path = PathConfig.parse_obj(self.__dict__["path"])
        self.joblib = JobLibConfig.parse_obj(self.__dict__["joblib"])

        self.dotenv.HYFI_PROJECT_NAME = self.project_name
        self.dotenv.HYFI_TASK_NAME = self.task_name
        self.dotenv.HYFI_PROJECT_DESC = self.project_description
        self.dotenv.HYFI_PROJECT_ROOT = self.project_root
        self.dotenv.HYFI_PROJECT_WORKSPACE_NAME = self.project_workspace_name
        self.dotenv.HYFI_GLOBAL_ROOT = self.global_hyfi_root
        self.dotenv.HYFI_GLOBAL_WORKSPACE_NAME = self.global_workspace_name
        self.dotenv.HYFI_NUM_WORKERS = self.num_workers
        self.dotenv.HYFI_VERBOSE = self.verbose
        self.dotenv.CACHED_PATH_CACHE_ROOT = str(self.path.cache_dir / "cached_path")
        self.init_wandb()
        if self.use_huggingface_hub:
            self.init_huggingface_hub()

    def init_wandb(self):
        if self.path is None:
            raise ValueError("Path object not initialized")
        if self.dotenv is None:
            raise ValueError("DotEnv object not initialized")

        self.dotenv.WANDB_DIR = str(self.path.log_dir)
        project_name = self.project_name.replace("/", "-").replace("\\", "-")
        self.dotenv.WANDB_PROJECT = project_name
        task_name = self.task_name.replace("/", "-").replace("\\", "-")
        notebook_name = self.path.log_dir / f"{task_name}-nb"
        notebook_name.mkdir(parents=True, exist_ok=True)
        self.dotenv.WANDB_NOTEBOOK_NAME = str(notebook_name)
        self.dotenv.WANDB_SILENT = str(not self.verbose)
        if self.use_wandb:
            try:
                import wandb  # type: ignore

                wandb.init(project=self.project_name)
            except ImportError:
                logger.warning(
                    "wandb is not installed, please install it to use wandb."
                )

    def init_huggingface_hub(self):
        """Initialize huggingface_hub"""
        try:
            from huggingface_hub import notebook_login  # type: ignore
            from huggingface_hub.hf_api import HfFolder  # type: ignore
        except ImportError:
            logger.warning(
                "huggingface_hub is not installed, please install it to use huggingface_hub."
            )
            return

        self.dotenv = DotEnvConfig()
        if (
            self.dotenv.HUGGING_FACE_HUB_TOKEN is None
            and self.dotenv.HF_USER_ACCESS_TOKEN is not None
        ):
            self.dotenv.HUGGING_FACE_HUB_TOKEN = self.dotenv.HF_USER_ACCESS_TOKEN

        local_token = HfFolder.get_token()
        if local_token is None:
            if NBs.is_notebook():
                notebook_login()
            else:
                logger.info(
                    "huggingface_hub.notebook_login() is only available in notebook,"
                    "set HUGGING_FACE_HUB_TOKEN manually"
                )

    @property
    def osenv(self):
        return os.environ

    @property
    def project_workspace_dir(self):
        if self.path is None:
            raise ValueError("Path object not initialized")
        _p = Path(self.path.project_workspace_root)
        _p.mkdir(parents=True, exist_ok=True)
        return _p.absolute()

    @property
    def project_dir(self):
        if self.path is None:
            raise ValueError("Path object not initialized")
        _p = Path(self.path.project_root)
        _p.mkdir(parents=True, exist_ok=True)
        return _p.absolute()

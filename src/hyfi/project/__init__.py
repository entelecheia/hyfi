import os
from pathlib import Path
from typing import Union

from hyfi.composer import BaseConfig, field_validator
from hyfi.dotenv import DotEnvConfig
from hyfi.joblib import JobLibConfig
from hyfi.path import PathConfig
from hyfi.utils.logging import LOGGING
from hyfi.utils.notebooks import NBs

logger = LOGGING.getLogger(__name__)


class ProjectConfig(BaseConfig):
    """Project Config"""

    _config_name_: str = "__init__"
    _config_group_: str = "project"
    # Project Config
    project_name: str = "hyfi"
    project_description: str = ""
    project_root: str = ""
    project_workspace_name: str = "workspace"
    global_hyfi_root: str = ""
    global_workspace_name: str = ".hyfi"
    num_workers: int = 1
    use_huggingface_hub: bool = False
    use_wandb: bool = False
    verbose: Union[bool, int] = False
    # Config Classes
    dotenv: DotEnvConfig = None  # type: ignore
    joblib: JobLibConfig = None  # type: ignore
    path: PathConfig = None  # type: ignore

    _property_set_methods_ = {
        "project_name": "set_project_name",
        "project_root": "set_project_root",
    }

    def set_project_root(self, val: Union[str, Path]):
        if (not self.project_root or self.project_root != val) and self.path:
            self.path.project_root = str(val)

    def set_project_name(self, val):
        if (not self.project_name or self.project_name != val) and self.path:
            self.path.project_name = val

    @field_validator("project_name")
    def _validate_project_name(cls, v):
        if v is None:
            raise ValueError("Project name must be specified.")
        return v

    @field_validator("verbose")
    def _validate_verbose(cls, v):
        if isinstance(v, str):
            if v.lower() in {"true", "1"}:
                v = True
            elif v.lower() in {"false", "0"}:
                v = False
            else:
                raise ValueError("verbose must be a boolean or a string of 0 or 1")
        return v

    def __init__(self, **config_kwargs):
        super().__init__(**config_kwargs)
        self.initialize()

    def initialize(self):
        logger.debug("Initializing Project Config: %s", self.project_name)
        self.dotenv = DotEnvConfig()

        self.dotenv.HYFI_PROJECT_NAME = self.project_name
        self.dotenv.HYFI_PROJECT_DESC = self.project_description
        self.dotenv.HYFI_PROJECT_ROOT = self.project_root
        self.dotenv.HYFI_PROJECT_WORKSPACE_NAME = self.project_workspace_name
        self.dotenv.HYFI_GLOBAL_ROOT = self.global_hyfi_root
        self.dotenv.HYFI_GLOBAL_WORKSPACE_NAME = self.global_workspace_name
        self.dotenv.HYFI_NUM_WORKERS = self.num_workers
        self.dotenv.HYFI_VERBOSE = self.verbose
        self.dotenv.CACHED_PATH_CACHE_ROOT = str(self.path.cache_dir / "cached_path")

        if self.joblib:
            self.joblib.init_backend()
        else:
            logger.warning("JoblibConfig not initialized")

        self.init_wandb()
        if self.use_huggingface_hub:
            self.init_huggingface_hub()

    def init_wandb(self):
        if self.path is None:
            raise ValueError("Path object not initialized")
        if self.dotenv is None:
            raise ValueError("DotEnv object not initialized")

        if not self.use_wandb:
            return
        try:
            self._init_wandb()
        except ImportError:
            logger.warning("wandb is not installed, please install it to use wandb.")

    def _init_wandb(self):
        import wandb  # type: ignore

        self.dotenv.WANDB_DIR = str(self.path.log_dir)
        project_name = self.project_name.replace("/", "-").replace("\\", "-")
        self.dotenv.WANDB_PROJECT = project_name
        notebook_name = self.path.log_dir / f"{project_name}-nb"
        notebook_name.mkdir(parents=True, exist_ok=True)
        self.dotenv.WANDB_NOTEBOOK_NAME = str(notebook_name)
        self.dotenv.WANDB_SILENT = str(not self.verbose)

        wandb.init(project=project_name)

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
    def root_dir(self) -> Path:
        return self.path.root_dir if self.path else Path(self.project_root)

    @property
    def workspace_dir(self) -> Path:
        return (
            self.path.workspace_dir
            if self.path
            else self.root_dir / self.project_workspace_name
        )

    @property
    def global_root_dir(self) -> Path:
        return self.path.global_root_dir if self.path else Path(self.global_hyfi_root)

    @property
    def global_workspace_dir(self) -> Path:
        return (
            self.path.global_workspace_dir
            if self.path
            else self.global_root_dir / self.global_workspace_name
        )

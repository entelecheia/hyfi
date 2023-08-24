import os
from pathlib import Path
from typing import Optional, Union

from hyfi.composer import BaseConfig, Composer, field_validator
from hyfi.env import ProjectEnv
from hyfi.joblib import JobLib
from hyfi.path.project import ProjectPath

logger = Composer.getLogger(__name__)


class Project(BaseConfig, Composer):
    """Project Config"""

    _config_name_: str = "__init__"
    _config_group_: str = "/project"
    # Project Config
    project_name: str = "hyfi"
    project_description: Optional[str] = None
    project_root: str = "."
    project_workspace_name: str = "workspace"
    global_hyfi_root: str = "."
    global_workspace_name: str = ".hyfi"
    num_workers: int = 1
    use_huggingface_hub: bool = False
    use_wandb: bool = False
    verbose: Union[bool, int] = False
    # Config Classes
    env: ProjectEnv = None
    joblib: Optional[JobLib] = None
    path: ProjectPath = None

    _property_set_methods_ = {
        "project_name": "set_project_name",
        "project_root": "set_project_root",
    }

    def set_project_root(self, val: Union[str, Path]):
        if not self.project_root or self.project_root != val:
            self.path.project_root = str(val)

    def set_project_name(self, val):
        if not self.project_name or self.project_name != val:
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
        self.env = ProjectEnv()

        self.env.HYFI_PROJECT_NAME = self.project_name
        if self.project_description:
            self.env.HYFI_PROJECT_DESC = self.project_description
        if self.project_root:
            self.env.HYFI_PROJECT_ROOT = self.project_root
        if self.project_workspace_name:
            self.env.HYFI_PROJECT_WORKSPACE_NAME = self.project_workspace_name
        if self.global_hyfi_root:
            self.env.HYFI_GLOBAL_ROOT = self.global_hyfi_root
        if self.global_workspace_name:
            self.env.HYFI_GLOBAL_WORKSPACE_NAME = self.global_workspace_name
        if self.num_workers:
            self.env.HYFI_NUM_WORKERS = self.num_workers
        self.env.HYFI_VERBOSE = self.verbose

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
        if self.env is None:
            raise ValueError("Env object not initialized")

        if not self.use_wandb:
            return
        try:
            self._init_wandb()
        except ImportError:
            logger.warning("wandb is not installed, please install it to use wandb.")

    def _init_wandb(self):
        import wandb  # type: ignore

        self.env.WANDB_DIR = str(self.path.log_dir)
        project_name = self.project_name.replace("/", "-").replace("\\", "-")
        self.env.WANDB_PROJECT = project_name
        notebook_name = self.path.log_dir / f"{project_name}-nb"
        notebook_name.mkdir(parents=True, exist_ok=True)
        self.env.WANDB_NOTEBOOK_NAME = str(notebook_name)
        self.env.WANDB_SILENT = str(not self.verbose)

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

        self.env = ProjectEnv()
        if (
            self.env.HUGGING_FACE_HUB_TOKEN is None
            and self.env.HF_USER_ACCESS_TOKEN is not None
        ):
            self.env.HUGGING_FACE_HUB_TOKEN = self.env.HF_USER_ACCESS_TOKEN

        local_token = HfFolder.get_token()
        if local_token is None:
            if Project.is_notebook():
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
        self.path.project_root = self.project_root
        return self.path.root_dir

    @property
    def workspace_dir(self) -> Path:
        self.path.project_workspace_name = self.project_workspace_name
        return self.path.workspace_dir

    @property
    def global_root_dir(self) -> Path:
        self.path.global_hyfi_root = self.global_hyfi_root
        return self.path.global_root_dir

    @property
    def global_workspace_dir(self) -> Path:
        self.path.global_workspace_name = self.global_workspace_name
        return self.path.global_workspace_dir

    def get_path(
        self,
        path_name: str,
        base_dir: Optional[Union[Path, str]] = None,
        ensure_exists: bool = False,
    ) -> Optional[Path]:
        """
        Get the path to a directory or file.
        """
        return (
            self.path.get_path(
                path_name, base_dir=base_dir, ensure_exists=ensure_exists
            )
            if self.path
            else None
        )

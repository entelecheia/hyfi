import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import hydra
from omegaconf import DictConfig, ListConfig, OmegaConf, SCMode
from pydantic import BaseModel, BaseSettings, SecretStr, root_validator, validator
from pydantic.env_settings import SettingsSourceCallable

from .utils.batch import batcher
from .utils.env import _check_and_set_value, expand_posix_vars, load_dotenv
from .utils.logging import getLogger, setLogger
from .utils.notebook import is_notebook, load_extentions, set_matplotlib_formats

logger = getLogger(__name__)

__hydra_version_base__ = "1.2"

DictKeyType = Union[str, bytes, int, Enum, float, bool]


def __version__():
    """Returns the version of HyFI"""
    from ._version import __version__

    return __version__


def _select(
    cfg: Any,
    key: str,
    *,
    default: Any = None,
    throw_on_resolution_failure: bool = True,
    throw_on_missing: bool = False,
):
    key = key.replace("/", ".")
    return OmegaConf.select(
        cfg,
        key=key,
        default=default,
        throw_on_resolution_failure=throw_on_resolution_failure,
        throw_on_missing=throw_on_missing,
    )


def _to_dict(
    cfg: Any,
) -> Any:
    if isinstance(cfg, dict):
        cfg = _to_config(cfg)
    if isinstance(cfg, (DictConfig, ListConfig)):
        return OmegaConf.to_container(
            cfg,
            resolve=True,
            throw_on_missing=False,
            structured_config_mode=SCMode.DICT,
        )
    return cfg


def _to_config(
    cfg: Any,
) -> Union[DictConfig, ListConfig]:
    return OmegaConf.create(cfg)


class AboutConfig(BaseModel):
    """About Configuration"""

    __package_name__: str = "hyfi"
    name: str = "HyFI"
    authors: str = "Young Joon Lee <entelecheia@hotmail.com>"
    description: str = (
        "Hydra Fast Interface (Hydra and Pydantic based interface framework)"
    )
    homepage: str = "https://hyfi.entelecheia.ai"
    license: str = "MIT"
    version: str = "0.0.0"

    class Config:
        extra = "allow"
        underscore_attrs_are_private = False

    @property
    def config_module(self) -> str:
        return f"{self.__package_name__}.conf"

    @property
    def config_path(self) -> str:
        return f"pkg://{self.config_module}"


__about__ = AboutConfig()


class DistFramwork(BaseModel):
    """Distributed Framework Configuration"""

    backend: str = "joblib"
    initialize: bool = False
    num_workers: int = 1


class BatcherConfig(BaseModel):
    """Batcher Configuration"""

    procs: int = 1
    minibatch_size: int = 1_000
    backend: str = "joblib"
    task_num_cpus: int = 1
    task_num_gpus: int = 0
    verbose: int = 10


class JobLibConfig(BaseModel):
    """JobLib Configuration"""

    config_name: str = "__init__"
    distributed_framework: DistFramwork = DistFramwork()
    batcher: BatcherConfig = BatcherConfig()
    __initilized__: bool = False

    class Config:
        extra = "allow"
        underscore_attrs_are_private = True

    def __init__(
        self,
        config_name: str = "__init__",
        **data: Any,
    ):
        if not data:
            logger.debug(
                "There are no arguments to initilize a config, using default config."
            )
            data = _compose(
                f"joblib={config_name}", config_module=__about__.config_module
            )  # type: ignore
        super().__init__(config_name=config_name, **data)

    def init_backend(
        self,
    ):
        """Initialize the backend for joblib"""
        if self.distributed_framework.initialize:
            backend_handle = None
            backend = self.distributed_framework.backend

            if backend == "dask":
                from dask.distributed import Client  # type: ignore

                dask_cfg = {"n_workers": self.distributed_framework.num_workers}
                logger.info(f"initializing dask client with {dask_cfg}")
                client = Client(**dask_cfg)
                logger.debug(client)

            elif backend == "ray":
                import ray  # type: ignore

                ray_cfg = {"num_cpus": self.distributed_framework.num_workers}
                logger.info(f"initializing ray with {ray_cfg}")
                ray.init(**ray_cfg)
                backend_handle = ray

            batcher.batcher_instance = batcher.Batcher(
                backend_handle=backend_handle, **self.batcher.dict()
            )
            logger.info(f"initialized batcher with {batcher.batcher_instance}")
        self.__initilized__ = True

    def stop_backend(self):
        """Stop the backend for joblib"""
        backend = self.distributed_framework.backend
        if batcher.batcher_instance:
            logger.info("stopping batcher")
            del batcher.batcher_instance

        logger.info("stopping distributed framework")
        if self.distributed_framework.initialize:
            if backend == "ray":
                try:
                    import ray  # type: ignore

                    if ray.is_initialized():
                        ray.shutdown()
                        logger.info("shutting down ray")
                except ImportError:
                    logger.warning("ray is not installed")

            elif backend == "dask":
                try:
                    from dask.distributed import Client  # type: ignore

                    if Client.initialized():
                        Client.close()
                        logger.info("shutting down dask client")
                except ImportError:
                    logger.warning("dask is not installed")


class PathConfig(BaseModel):
    config_name: str = "__init__"
    # internal paths for hyfi
    home: str = ""
    hyfi: str = ""
    resources: str = ""
    runtime: str = ""
    # global paths
    global_workspace_root: str = ""
    global_data_root: str = ""
    global_archive: str = ""
    global_datasets: str = ""
    global_models: str = ""
    global_modules: str = ""
    global_library: str = ""
    global_cache: str = ""
    global_tmp: str = ""
    # project specific paths
    project_root: str = ""
    project_data_root: str = ""
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

    def __init__(
        self,
        config_name: str = "__init__",
        **data: Any,
    ):
        """
        Initialize the config. This is the base implementation of __init__. You can override this in your own subclass if you want to customize the initilization of a config by passing a keyword argument ` data `.

        Args:
                config_name: The name of the config to initialize
                data: The data to initialize
        """
        # Initialize the config module.
        if not data:
            logger.debug(
                "There are no arguments to initilize a config, using default config %s",
                config_name,
            )
            data = _compose(
                f"path={config_name}", config_module=__about__.config_module
            )  # type: ignore
        super().__init__(config_name=config_name, **data)

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


class DotEnvConfig(BaseSettings):
    """Environment variables for HyFI"""

    config_name: str = "__init__"

    DOTENV_FILENAME: Optional[str] = ".env"
    DOTENV_DIR: Optional[str] = ""
    DOTENV_PATH: Optional[str] = ""
    # Internal
    HYFI_RESOURCE_DIR: Optional[str] = ""
    HYFI_GLOBAL_WORKSPACE_ROOT: Optional[str] = ""
    HYFI_GLOBAL_DATA_ROOT: Optional[str] = ""
    HYFI_PROJECT_NAME: Optional[str] = ""
    HYFI_TASK_NAME: Optional[str] = ""
    HYFI_PROJECT_ROOT: Optional[str] = ""
    HYFI_PROJECT_DATA_ROOT: Optional[str] = ""
    HYFI_LOG_LEVEL: Optional[str] = "WARNING"
    HYFI_VERBOSE: Optional[Union[bool, str, int]] = False
    NUM_WORKERS: Optional[int] = 1
    CACHED_PATH_CACHE_ROOT: Optional[str] = ""
    # For other packages
    CUDA_DEVICE_ORDER: Optional[str] = "PCI_BUS_ID"
    CUDA_VISIBLE_DEVICES: Optional[str] = ""
    WANDB_PROJECT: Optional[str] = ""
    WANDB_DISABLED: Optional[str] = ""
    WANDB_DIR: Optional[str] = ""
    WANDB_NOTEBOOK_NAME: Optional[str] = ""
    WANDB_SILENT: Optional[Union[bool, str]] = False
    LABEL_STUDIO_SERVER: Optional[str] = ""
    KMP_DUPLICATE_LIB_OK: Optional[str] = "True"
    TOKENIZERS_PARALLELISM: Optional[Union[bool, str]] = False
    # API Keys and Tokens
    WANDB_API_KEY: Optional[SecretStr] = None
    HUGGING_FACE_HUB_TOKEN: Optional[SecretStr] = None
    OPENAI_API_KEY: Optional[SecretStr] = None
    ECOS_API_KEY: Optional[SecretStr] = None
    FRED_API_KEY: Optional[SecretStr] = None
    NASDAQ_API_KEY: Optional[SecretStr] = None
    HF_USER_ACCESS_TOKEN: Optional[SecretStr] = None
    LABEL_STUDIO_USER_TOKEN: Optional[SecretStr] = None

    class Config:
        env_prefix = ""
        env_nested_delimiter = "__"
        case_sentive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        validate_assignment = True
        extra = "allow"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            load_dotenv()
            return env_settings, file_secret_settings, init_settings

    @root_validator()
    def _check_and_set_values(cls, values):
        global_workspace_root = values.get("HYFI_GLOBAL_WORKSPACE_ROOT")
        global_data_root = values.get("HYFI_GLOBAL_DATA_ROOT")
        if global_workspace_root and not global_data_root:
            global_data_root = os.path.join(global_workspace_root, "data")
            values["HYFI_GLOBAL_DATA_ROOT"] = global_data_root
        project_name = values.get("HYFI_PROJECT_NAME")
        project_root = values.get("HYFI_PROJECT_ROOT")
        dotenv_dir = values.get("DOTENV_DIR")
        if not project_root:
            if global_workspace_root and project_name:
                project_root = os.path.join(
                    global_workspace_root, "projects", project_name
                )
                values["HYFI_PROJECT_ROOT"] = project_root
            elif dotenv_dir and Path(dotenv_dir).is_dir():
                project_root = dotenv_dir
                values["HYFI_PROJECT_ROOT"] = project_root
        project_data_root = values.get("HYFI_PROJECT_DATA_ROOT")
        if project_root and not project_data_root:
            project_data_root = os.path.join(project_root, "workspace")
            values["HYFI_PROJECT_DATA_ROOT"] = project_data_root

        for k, v in values.items():
            if v is not None:
                old_value = os.getenv(k.upper())
                if old_value is None or old_value != str(v):
                    os.environ[k.upper()] = str(v)
                    logger.debug(f"Set environment variable {k.upper()}={v}")
        return values


class ProjectConfig(BaseModel):
    """Project Config"""

    config_name: str = "__init__"
    project_name: str = "hyfi-project"
    task_name: str = ""
    project_description: str = ""
    project_root: str = ""
    project_data_root: str = ""
    global_workspace_root: str = ""
    global_data_root: str = ""
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

    def __init__(
        self,
        config_name: str = "__init__",
        **data: Any,
    ):
        if not data:
            logger.debug(
                "There are no arguments to initilize a config, using default config."
            )
            data = _compose(
                f"project={config_name}", config_module=__about__.config_module
            )  # type: ignore
        super().__init__(config_name=config_name, **data)

    @validator("project_name", allow_reuse=True)
    def _validate_project_name(cls, v):
        if v is None:
            raise ValueError("Project name must be specified.")
        return v

    @property
    def environ(self):
        return os.environ

    @property
    def project_data_dir(self):
        if self.path is None:
            raise ValueError("Path object not initialized")
        _p = Path(self.path.project_data_root)
        _p.mkdir(parents=True, exist_ok=True)
        return _p.absolute()

    @property
    def project_dir(self):
        if self.path is None:
            raise ValueError("Path object not initialized")
        _p = Path(self.path.project_root)
        _p.mkdir(parents=True, exist_ok=True)
        return _p.absolute()

    def init_project(self):
        self.dotenv = DotEnvConfig()
        if self.path is None:
            self.path = PathConfig()
        if self.joblib is None:
            self.joblib = JobLibConfig()

        if self.dotenv.HYFI_VERBOSE is not None:
            self.verbose = int(self.dotenv.HYFI_VERBOSE)
        self.dotenv.HYFI_GLOBAL_WORKSPACE_ROOT = str(self.path.global_workspace_root)
        self.dotenv.HYFI_GLOBAL_DATA_ROOT = str(self.path.global_data_root)
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
            if is_notebook():
                notebook_login()
            else:
                logger.info(
                    "huggingface_hub.notebook_login() is only available in notebook,"
                    "set HUGGING_FACE_HUB_TOKEN manually"
                )


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
        project_root: str = "",
        project_data_root: str = "",
        global_workspace_root: str = "",
        global_data_root: str = "",
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
        if project_root:
            envs.HYFI_PROJECT_ROOT = expand_posix_vars(project_root)
        if project_data_root:
            envs.HYFI_PROJECT_DATA_ROOT = expand_posix_vars(project_data_root)
        if global_workspace_root:
            envs.HYFI_GLOBAL_WORKSPACE_ROOT = expand_posix_vars(global_workspace_root)
        if global_data_root:
            envs.HYFI_GLOBAL_DATA_ROOT = expand_posix_vars(global_data_root)
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


class Dummy:
    def __call__(self, *args, **kwargs):
        return Dummy()


def _compose(
    config_group: Union[str, None] = None,
    overrides: Union[List[str], None] = None,
    *,
    return_as_dict: bool = False,
    throw_on_resolution_failure: bool = True,
    throw_on_missing: bool = False,
    config_name: Union[str, None] = None,
    config_module: Union[str, None] = None,
    verbose: bool = False,
) -> Union[DictConfig, Dict]:  # sourcery skip: low-code-quality
    """
    Compose your configuration from config groups and overrides (overrides=["override_name"])

    :param overrides: List of overrides to apply
    :param config_group: Config group name to select ('config_group=name')
    :param return_as_dict: Return the composed config as a dict
    :param throw_on_resolution_failure: Throw if resolution fails
    :param throw_on_missing: Throw if a config is missing
    :param config_name: Name of the config to compose
    :param verbose: Print the composed config

    :return: The composed config
    """
    if overrides is None:
        overrides = []
    config_module = config_module or __global_config__.hyfi_config_module
    # if verbose:
    logger.info("config_module: %s", config_module)
    is_initialized = hydra.core.global_hydra.GlobalHydra.instance().is_initialized()  # type: ignore
    if config_group:
        _task = config_group.split("=")
        if len(_task) == 2:
            key, value = _task
        else:
            key = _task[0]
            value = "default"
        config_group = f"{key}={value}"
    else:
        key = None
        value = None
    if key and value:
        if is_initialized:
            cfg = hydra.compose(config_name=config_name, overrides=overrides)
        else:
            with hydra.initialize_config_module(
                config_module=config_module, version_base=__hydra_version_base__
            ):
                cfg = hydra.compose(config_name=config_name, overrides=overrides)
        cfg = _select(
            cfg,
            key=key,
            default=None,
            throw_on_missing=False,
            throw_on_resolution_failure=False,
        )
        override = config_group if cfg is not None else f"+{config_group}"
        if isinstance(override, str):
            if overrides:
                overrides.append(override)
            else:
                overrides = [override]
    # if verbose:
    logger.info(f"compose config with overrides: {overrides}")
    if is_initialized:
        if verbose:
            logger.info("Hydra is already initialized")
        cfg = hydra.compose(config_name=config_name, overrides=overrides)
    else:
        with hydra.initialize_config_module(
            config_module=config_module, version_base=__hydra_version_base__
        ):
            cfg = hydra.compose(config_name=config_name, overrides=overrides)

    if key and key != "task":
        cfg = _select(
            cfg,
            key=key,
            default=None,
            throw_on_missing=throw_on_missing,
            throw_on_resolution_failure=throw_on_resolution_failure,
        )
    logger.debug("Composed config: %s", OmegaConf.to_yaml(cfg))
    return _to_dict(cfg) if return_as_dict and isinstance(cfg, DictConfig) else cfg

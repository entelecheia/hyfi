"""
Hyfi configuration file.
"""
from pathlib import Path
from typing import Dict, List, Optional, Union

from omegaconf import DictConfig

from hyfi.about import About
from hyfi.composer import (
    BaseModel,
    ConfigDict,
    FieldValidationInfo,
    PrivateAttr,
    field_validator,
)
from hyfi.core import global_hyfi
from hyfi.project import Project
from hyfi.utils import UTILs

logger = UTILs.getLogger(__name__)

ConfigType = Union[DictConfig, Dict]

__default_project_root__ = "."
__default_workspace_name__ = "workspace"


class HyFIConfig(BaseModel, UTILs):
    """HyFI root config class.  This class is used to store the configuration"""

    _config_name_: str = "config"
    _config_group_: str = "/"

    debug_mode: bool = False
    noop: bool = False
    dryrun: bool = False
    resolve: bool = False
    verbose: bool = False
    logging_level: str = "WARNING"

    hydra: Optional[ConfigType] = None

    about: Optional[ConfigType] = None
    copier: Optional[ConfigType] = None
    project: Optional[ConfigType] = None
    pipeline: Optional[ConfigType] = None
    task: Optional[ConfigType] = None
    variables: Optional[ConfigType] = None
    workflow: Optional[ConfigType] = None
    tasks: Optional[List[str]] = None
    workflows: Optional[List[str]] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="allow",
    )  # type: ignore

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


class GlobalConfig(UTILs):
    """HyFI global config class.  This class is used to store the global configuration"""

    __config__: Optional[HyFIConfig] = None

    _about_: Optional[About] = None
    _project_: Optional[Project] = None
    _version_: str = PrivateAttr(global_hyfi.version)

    def __init__(self, **config_kwargs):
        if config_kwargs:
            self.__config__ = HyFIConfig(**config_kwargs)

    @property
    def about(self) -> About:
        if self._about_ is None:
            config_name = (
                "__init__"
                if global_hyfi.package_name == "hyfi"
                else global_hyfi.package_name
            )
            kwargs = {"_config_name_": config_name}
            self._about_ = About(**kwargs)
        return self._about_

    @property
    def project(self) -> Project:
        return self._project_

    def inititialize(
        self,
        project_name: Optional[str] = None,
        project_description: Optional[str] = None,
        project_root: Optional[str] = None,
        project_workspace_name: Optional[str] = None,
        global_hyfi_root: Optional[str] = None,
        global_workspace_name: Optional[str] = None,
        num_workers: Optional[int] = None,
        logging_level: Optional[str] = None,
        plugins: Optional[List[str]] = None,
        user_config_path: Optional[str] = None,
        dotenv_file: Optional[str] = None,
        secrets_dir: Optional[str] = None,
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
            plugins: A list of plugins to load. e.g. `["hyfi.conf"]`
            user_config_path: Path to the user configuration directory. e.g. `./config`
            config_dirname: Name of the configuration directory. e.g. `conf`
            dotenv_file: Name of the dotenv file. e.g. `.env`
            secrets_dir: Name of the secrets directory. e.g. `secrets`
            reinit: Whether to reinitialize the global config.
            autotime: Whether to automatically set time and / or keep track of run times.
            retina: Whether to use retina or not.
            verbose: Enables or disables logging
        """
        if self.project and not reinit:
            return
        # Set the log level to the given log level.
        if logging_level:
            GlobalConfig.setLogger(logging_level)
            logger.setLevel(logging_level)

        global_hyfi.reinitialize(
            plugins=plugins,
            user_config_path=user_config_path,
            dotenv_file=dotenv_file,
            secrets_dir=secrets_dir,
        )

        # Load the extentions for the autotime extension.
        if autotime:
            GlobalConfig.load_extentions(exts=["autotime"])
        # Set the retina matplotlib formats.
        if retina:
            GlobalConfig.set_matplotlib_formats("retina")
        if project_name:
            project_kwargs["project_name"] = project_name
        if project_description:
            project_kwargs["project_description"] = project_description
        if project_root:
            project_kwargs["project_root"] = project_root
        if project_workspace_name:
            project_kwargs["project_workspace_name"] = project_workspace_name
        # Expand the hyfi_root environment variable.
        if global_hyfi_root:
            project_kwargs["global_hyfi_root"] = global_hyfi_root
        if global_workspace_name:
            project_kwargs["global_workspace_name"] = global_workspace_name
        if num_workers:
            project_kwargs["num_workers"] = num_workers
        project_kwargs["verbose"] = verbose

        self._project_ = Project(**project_kwargs)
        logger.info("HyFi project [%s] initialized", self._project_.project_name)

    def terminate(self) -> None:
        """
        Terminate hyfi config by stopping joblib

        Returns:
            True if successful False
        """
        # Stop the backend if the joblib is running.
        if self.project and self.project.joblib:
            self.project.joblib.stop_backend()

    def __repr__(self):
        """
        Returns a string representation of GlobalConfig.
        """
        return f"GlobalConfig(project={self.project})"

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return self.__repr__()

    @property
    def app_version(self):
        """
        Get the version of the application.
        """
        return global_hyfi.version

    @property
    def app_name(self):
        """
        Get the name of the application.
        """
        return self.about.name

    @property
    def package_name(self):
        """
        Get the name of the package.
        """
        return global_hyfi.package_name

    def print_about(self, **kwargs):
        if not kwargs:
            config_name = (
                "__init__"
                if global_hyfi.package_name == "hyfi"
                else global_hyfi.package_name
            )
            kwargs = {"_config_name_": config_name}
        self._about_ = About(**kwargs)
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
        ensure_exists: bool = False,
    ) -> Optional[Path]:
        """
        Get the path to a directory or file.
        """
        return (
            self.project.get_path(
                path_name, base_dir=base_dir, ensure_exists=ensure_exists
            )
            if self.project
            else None
        )


global_config = GlobalConfig()


class GlobalConfigResolver:
    @staticmethod
    def __project_root_path__() -> str:
        """Global HyFI config path for the project root."""
        return str(global_config.project_dir or "")

    @staticmethod
    def __project_workspace_path__() -> str:
        """Global HyFI config path for the project workspace directory."""
        return str(global_config.project_workspace_dir or "")

    @staticmethod
    def __get_path__(path_name: str, base_dir: Optional[str] = None) -> str:
        """
        Get the path to a directory or file.
        """
        return str(global_config.get_path(path_name, base_dir=base_dir) or "")

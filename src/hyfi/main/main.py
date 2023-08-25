"""
    This module contains the primary class for the hyfi config package, HyFI,
    as well as various utility functions and imports.
"""
import os
import random
from typing import Any, Dict, List, Optional, Union

import hydra
from omegaconf import DictConfig, OmegaConf

from hyfi.cached_path import cached_path
from hyfi.composer import BaseConfig, Composer
from hyfi.copier import Copier
from hyfi.core import GlobalHyFIResolver, global_hyfi
from hyfi.env import Env
from hyfi.graphics import GRAPHICs
from hyfi.joblib import BATCHER, JobLib
from hyfi.pipeline import PIPELINEs
from hyfi.project import Project
from hyfi.task import Task
from hyfi.workflow import Workflow

from .config import GlobalConfigResolver, HyFIConfig, global_config

logger = Composer.getLogger(__name__)

ConfigType = Union[DictConfig, Dict]

OmegaConf.register_new_resolver("__hyfi_path__", GlobalHyFIResolver.__hyfi_path__)
OmegaConf.register_new_resolver("__hyfi_version__", GlobalHyFIResolver.__hyfi_version__)
OmegaConf.register_new_resolver("__package_name__", GlobalHyFIResolver.__package_name__)
OmegaConf.register_new_resolver("__package_path__", GlobalHyFIResolver.__package_path__)
OmegaConf.register_new_resolver("__app_version__", GlobalHyFIResolver.__app_version__)
OmegaConf.register_new_resolver("__version__", GlobalHyFIResolver.__app_version__)
OmegaConf.register_new_resolver(
    "__config_module_path__", GlobalHyFIResolver.__config_module_path__
)
OmegaConf.register_new_resolver(
    "__user_config_path__", GlobalHyFIResolver.__user_config_path__
)
OmegaConf.register_new_resolver("__home_path__", GlobalHyFIResolver.__home_path__)
OmegaConf.register_new_resolver(
    "__project_root_path__", GlobalConfigResolver.__project_root_path__
)
OmegaConf.register_new_resolver(
    "__project_workspace_path__", GlobalConfigResolver.__project_workspace_path__
)
OmegaConf.register_new_resolver("__get_path__", GlobalConfigResolver.__get_path__)
OmegaConf.register_new_resolver("today", Composer.today)
OmegaConf.register_new_resolver("to_datetime", Composer.strptime)
OmegaConf.register_new_resolver("iif", lambda cond, t, f: t if cond else f)
OmegaConf.register_new_resolver("alt", lambda val, alt: val or alt)
OmegaConf.register_new_resolver("randint", random.randint, use_cache=True)
OmegaConf.register_new_resolver("get_method", hydra.utils.get_method)
OmegaConf.register_new_resolver("get_original_cwd", Composer.getcwd)
OmegaConf.register_new_resolver("exists", Composer.exists)
OmegaConf.register_new_resolver("join_path", Composer.join_path)
OmegaConf.register_new_resolver("mkdir", Composer.mkdir)
OmegaConf.register_new_resolver("dirname", os.path.dirname)
OmegaConf.register_new_resolver("basename", os.path.basename)
OmegaConf.register_new_resolver("check_path", Composer.check_path)
OmegaConf.register_new_resolver("cached_path", cached_path)
OmegaConf.register_new_resolver(
    "lower_case_with_underscores", Composer.lower_case_with_underscores
)
OmegaConf.register_new_resolver("dotenv_values", Composer.dotenv_values)


class Variables(BaseConfig):
    _config_name_: str = "__init__"
    _config_group_: str = "/variables"

    hyfi_path: str = GlobalHyFIResolver.__hyfi_path__
    hyfi_version: str = GlobalHyFIResolver.__hyfi_version__
    package_name: str = GlobalHyFIResolver.__package_name__
    package_path: str = GlobalHyFIResolver.__package_path__
    app_version: str = GlobalHyFIResolver.__app_version__
    version: str = GlobalHyFIResolver.__app_version__
    config_module_path: str = GlobalHyFIResolver.__config_module_path__
    user_config_path: str = GlobalHyFIResolver.__user_config_path__
    home_path: str = GlobalHyFIResolver.__home_path__
    project_root_path: str = GlobalConfigResolver.__project_root_path__
    project_workspace_path: str = GlobalConfigResolver.__project_workspace_path__


class HyFI(
    BATCHER,
    Composer,
    GRAPHICs,
    PIPELINEs,
):
    """Primary class for the hyfi config package"""

    __config__: Optional[HyFIConfig] = None
    __variables__: Optional[Variables] = None

    __version__ = GlobalHyFIResolver.__hyfi_version__()
    __hyfi_path__ = GlobalHyFIResolver.__hyfi_path__()
    __home_path__ = GlobalHyFIResolver.__home_path__()
    __package_name__ = GlobalHyFIResolver.__package_name__()
    __package_path__ = GlobalHyFIResolver.__package_path__()
    __app_version__ = GlobalHyFIResolver.__app_version__()

    def __init__(self, **config_kwargs):
        if config_kwargs:
            self.__config__ = HyFIConfig(**config_kwargs)
            if self.__config__.project:
                self.initialize(**self.__config__.project)

    @property
    def config(self) -> HyFIConfig:
        """Get the global config."""
        return self.__config__

    @property
    def project(self) -> Optional[Project]:
        """Get the project."""
        if global_config.project:
            return global_config.project
        else:
            raise ValueError("Project not initialized.")

    @project.setter
    def project(self, project: Project) -> None:
        """Set the project."""
        global_config.project = project

    @staticmethod
    def set_project(project: Project) -> None:
        """
        Set the project.

        Args:
            project: Project to set.
        """
        logger.info(f"Setting the global project to {project.project_name}")
        global_config.project = project

    @staticmethod
    def initialize(
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
    ) -> "HyFI":
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
            logging_level: Log level for the log.
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
        global_config.inititialize(
            project_name=project_name,
            project_description=project_description,
            project_root=project_root,
            project_workspace_name=project_workspace_name,
            global_hyfi_root=global_hyfi_root,
            global_workspace_name=global_workspace_name,
            num_workers=num_workers,
            logging_level=logging_level,
            plugins=plugins,
            user_config_path=user_config_path,
            dotenv_file=dotenv_file,
            secrets_dir=secrets_dir,
            reinit=reinit,
            autotime=autotime,
            retina=retina,
            verbose=verbose,
            **HyFI.to_dict(project_kwargs),
        )
        return HyFI()

    @staticmethod
    def terminate() -> None:
        """
        Terminate the global config.

        Returns:
            bool: True if termination was successful, False otherwise.
        """
        global_config.terminate()

    @staticmethod
    def initialize_global_hyfi(
        package_path: str,
        version: str,
        plugins: Optional[List[str]] = None,
        user_config_path: Optional[str] = None,
        config_dirname: Optional[str] = None,
        dotenv_file: Optional[str] = None,
        secrets_dir: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Initializes the global HyFI instance.
        This function should be called before any other HyFI function.
        A plugin is a python module which contains a configuration module.

        Args:
            package_path: Path to the package root folder. e.g. `./src/hyfi`
            version: Version of the package. e.g. `0.1.0`
            plugins: A list of plugins to load. e.g. `["hyfi.conf"]`
            user_config_path: Path to the user configuration directory. e.g. `./config`
            config_dirname: Name of the configuration directory. e.g. `conf`
            dotenv_file: Name of the dotenv file. e.g. `.env`
            secrets_dir: Name of the secrets directory. e.g. `secrets`
            **kwargs: Additional arguments to be set as attributes.
        """
        global_hyfi.initialize(
            package_path=package_path,
            version=version,
            plugins=plugins,
            user_config_path=user_config_path,
            config_dirname=config_dirname,
            dotenv_file=dotenv_file,
            secrets_dir=secrets_dir,
            **kwargs,
        )

    @property
    def dryrun(self) -> bool:
        """Get the dryrun flag."""
        return self.config.dryrun or self.config.noop

    @property
    def variables(self) -> Variables:
        """Get the global variables."""
        if self.__variables__ is None:
            self.__variables__ = Variables()
        return self.__variables__

    @property
    def resolve(self) -> bool:
        """Get the resolve flag."""
        return self.config.resolve

    @property
    def verbose(self) -> bool:
        """Get the verbose flag."""
        return self.config.verbose or self.dryrun

    @property
    def app_name(self):
        """
        Get the name of the application.
        """
        return global_config.app_name

    @property
    def app_version(self):
        """
        Get the version of the application.
        """
        return global_config.app_version

    @staticmethod
    def print_about(**args) -> None:
        """Print the about information"""
        global_config.print_about(**args)

    @staticmethod
    def Variables(**kwargs) -> Variables:
        """
        Return the Variables.

        Args:
            **kwargs: Additional keyword arguments to pass to the Variables constructor.

        Returns:
            Variables: An instance of the Variables class.
        """
        return Variables(**kwargs)

    @staticmethod
    def JobLib(**kwargs) -> JobLib:
        """
        Return the joblib pipe.

        Args:
            **kwargs: Additional keyword arguments to pass to the JobLibConfig constructor.

        Returns:
            JobLibConfig: An instance of the JobLibConfig class.
        """
        return JobLib(**kwargs)

    @staticmethod
    def Env(**kwargs) -> Env:
        """
        Return the Env.

        Args:
            **kwargs: Additional keyword arguments to pass to the Env constructor.

        Returns:
            Env: An instance of the Env class.
        """
        return Env(**kwargs)

    @staticmethod
    def Task(**kwargs) -> Task:
        """
        Return the TaskConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the TaskConfig constructor.

        Returns:
            TaskConfig: An instance of the TaskConfig class.
        """
        return Task(**kwargs)

    @staticmethod
    def Workflow(**kwargs) -> Workflow:
        """
        Return the WorkflowConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the WorkflowConfig constructor.

        Returns:
            WorkflowConfig: An instance of the WorkflowConfig class.
        """
        return Workflow(**kwargs)

    ###############################
    # Pipeline related functions
    ###############################
    @staticmethod
    def run_command(**config):
        """Run a command"""
        return HyFI.run_config(config)

    @staticmethod
    def run(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        global_package=False,
        dryrun=False,
        **kwargs,
    ):
        """Run the config by composing it and running it"""
        if config_group:
            logger.info("Composing the HyFI config from config group %s", config_group)
            config = HyFI.compose_as_dict(
                config_group=config_group,
                overrides=overrides,
                config_data=config_data,
                global_package=global_package,
            )
        HyFI.run_config(config, dryrun=dryrun)

    @staticmethod
    def run_intantiatable(
        config: Dict[str, Any],
        dryrun=False,
    ):
        """Run the config by composing it and running it"""
        logger.info("Instantiating the HyFI config")
        if dryrun:
            print("\nDryrun is enabled, not running the HyFI config\n")
            return
        task = HyFI.instantiate(config)
        if task and getattr(task, "__call__", None):
            logger.info("The HyFI config is callable, running it")
            task()

    @staticmethod
    def run_config(
        config: Union[Dict[str, Any], DictConfig],
        dryrun=False,
    ):
        """Run the provided config"""
        config = HyFI.to_dict(config) if config else {}
        # Check if the config is instantiatable
        if HyFI.is_instantiatable(config):
            HyFI.run_intantiatable(config, dryrun=dryrun)
            return

        logger.info(
            "The HyFI config is not instantiatable, running HyFI task with the config"
        )
        # Run the HyFI task
        cmd_name = config.get("cmd_name")
        config_group = config.get("_config_group_", "")
        if not cmd_name:
            if config_group == "/workflow":
                cmd_name = "run_workflow"
            elif "task" in config:
                cmd_name = "run_task"
            elif "copier" in config:
                cmd_name = "copy_conf"

        if cmd_name == "run_workflow":
            workflow = HyFI.Workflow(**config)
            HyFI.run_workflow(workflow, dryrun=dryrun)
        elif cmd_name == "run_task":
            project = (
                HyFI.initialize(**config["project"]) if "project" in config else None
            )
            task = HyFI.Task(**config["task"])
            HyFI.run_task(task, project=project, dryrun=dryrun)
        elif cmd_name == "copy_conf":
            copier_cfg = config["copier"]
            copier_cfg["dryrun"] = dryrun
            with Copier(**copier_cfg) as worker:
                worker.run_copy()
        else:
            for _, cfg in config.items():
                if HyFI.is_instantiatable(cfg):
                    HyFI.run_intantiatable(cfg, dryrun)
                    return
            if not dryrun:
                HyFI.print_about(**config.get("about", {}))

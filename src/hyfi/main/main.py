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
from hyfi.composer import GENERATOR, Composer
from hyfi.copier import Copier
from hyfi.core import (
    __app_version__,
    __config_module_path__,
    __home_path__,
    __hyfi_path__,
    __hyfi_version__,
    __package_name__,
    __package_path__,
    __user_config_path__,
    global_hyfi,
)
from hyfi.dotenv import DotEnvConfig
from hyfi.graphics import GRAPHICs
from hyfi.joblib import BATCHER, JobLibConfig
from hyfi.pipeline import PIPELINEs
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils import LOGGING, DATASETs, ENVs, FUNCs, GPUs, IOLIBs, NBs, PKGs
from hyfi.workflow import WorkflowConfig

from .config import __project_root_path__, __project_workspace_path__, global_config

logger = LOGGING.getLogger(__name__)


OmegaConf.register_new_resolver("__hyfi_path__", __hyfi_path__)
OmegaConf.register_new_resolver("__hyfi_version__", __hyfi_version__)
OmegaConf.register_new_resolver("__package_name__", __package_name__)
OmegaConf.register_new_resolver("__package_path__", __package_path__)
OmegaConf.register_new_resolver("__app_version__", __app_version__)
OmegaConf.register_new_resolver("__version__", __app_version__)
OmegaConf.register_new_resolver("__config_module_path__", __config_module_path__)
OmegaConf.register_new_resolver("__user_config_path__", __user_config_path__)
OmegaConf.register_new_resolver("__home_path__", __home_path__)
OmegaConf.register_new_resolver("__project_root_path__", __project_root_path__)
OmegaConf.register_new_resolver(
    "__project_workspace_path__", __project_workspace_path__
)
OmegaConf.register_new_resolver("today", FUNCs.today)
OmegaConf.register_new_resolver("to_datetime", FUNCs.strptime)
OmegaConf.register_new_resolver("iif", lambda cond, t, f: t if cond else f)
OmegaConf.register_new_resolver("alt", lambda val, alt: val or alt)
OmegaConf.register_new_resolver("randint", random.randint, use_cache=True)
OmegaConf.register_new_resolver("get_method", hydra.utils.get_method)
OmegaConf.register_new_resolver("get_original_cwd", ENVs.getcwd)
OmegaConf.register_new_resolver("exists", IOLIBs.exists)
OmegaConf.register_new_resolver("join_path", IOLIBs.join_path)
OmegaConf.register_new_resolver("mkdir", IOLIBs.mkdir)
OmegaConf.register_new_resolver("dirname", os.path.dirname)
OmegaConf.register_new_resolver("basename", os.path.basename)
OmegaConf.register_new_resolver("check_path", IOLIBs.check_path)
OmegaConf.register_new_resolver("cached_path", cached_path)
OmegaConf.register_new_resolver(
    "lower_case_with_underscores", FUNCs.lower_case_with_underscores
)
OmegaConf.register_new_resolver("dotenv_values", ENVs.dotenv_values)


class HyFI(
    BATCHER,
    Composer,
    DATASETs,
    ENVs,
    FUNCs,
    GENERATOR,
    GPUs,
    GRAPHICs,
    IOLIBs,
    LOGGING,
    NBs,
    PIPELINEs,
    PKGs,
):
    """Primary class for the hyfi config package"""

    __version__ = __hyfi_version__()
    __hyfi_path__ = __hyfi_path__()
    __home_path__ = __home_path__()
    __package_name__ = __package_name__()
    __package_path__ = __package_path__()
    __app_version__ = __app_version__()

    def __init__(self) -> None:
        raise NotImplementedError("Use one of the static construction functions")

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

        Be careful!
        It does not check if the plugin is importable.

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

    @staticmethod
    def about(**args) -> None:
        """Print the about information"""
        global_config.print_about(**args)

    @staticmethod
    def init_project(
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
    ) -> ProjectConfig:
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
        global_config.init_project(
            project_name=project_name,
            project_description=project_description,
            project_root=project_root,
            project_workspace_name=project_workspace_name,
            global_hyfi_root=global_hyfi_root,
            global_workspace_name=global_workspace_name,
            num_workers=num_workers,
            log_level=log_level,
            reinit=reinit,
            autotime=autotime,
            retina=retina,
            verbose=verbose,
            **project_kwargs,
        )
        if global_config.project:
            return global_config.project
        else:
            raise ValueError("Project not initialized.")

    @staticmethod
    def set_project(project: ProjectConfig) -> None:
        """
        Set the project.

        Args:
            project: Project to set.
        """
        logger.info(f"Setting the global project to {project.project_name}")
        global_config.project = project

    @staticmethod
    def terminate() -> None:
        """
        Terminate the global config.

        Returns:
            bool: True if termination was successful, False otherwise.
        """
        global_config.terminate()

    @staticmethod
    def joblib(**kwargs) -> JobLibConfig:
        """
        Return the joblib pipe.

        Args:
            **kwargs: Additional keyword arguments to pass to the JobLibConfig constructor.

        Returns:
            JobLibConfig: An instance of the JobLibConfig class.
        """
        return JobLibConfig(**kwargs)

    @staticmethod
    def dotenv(**kwargs) -> DotEnvConfig:
        """
        Return the DotEnvConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the DotEnvConfig constructor.

        Returns:
            DotEnvConfig: An instance of the DotEnvConfig class.
        """
        return DotEnvConfig(**kwargs)

    @staticmethod
    def osenv():
        """
        Return the os environment variables as a dictionary.

        Returns:
            dict: A dictionary containing the os environment variables.
        """
        return os.environ

    @staticmethod
    def task(**kwargs) -> TaskConfig:
        """
        Return the TaskConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the TaskConfig constructor.

        Returns:
            TaskConfig: An instance of the TaskConfig class.
        """
        return TaskConfig(**kwargs)

    @staticmethod
    def workflow(**kwargs) -> WorkflowConfig:
        """
        Return the WorkflowConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the WorkflowConfig constructor.

        Returns:
            WorkflowConfig: An instance of the WorkflowConfig class.
        """
        return WorkflowConfig(**kwargs)

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
        if not isinstance(config, dict):
            raise ValueError("The config must be a dictionary")
        cmd_name = config.get("cmd_name")
        # Check if the config is instantiatable
        if HyFI.is_instantiatable(config):
            HyFI.run_intantiatable(config, dryrun=dryrun)
        else:
            logger.info(
                "The HyFI config is not instantiatable, running HyFI task with the config"
            )
            # Run the HyFI task
            config_group = config.get("_config_group_", "")
            if config_group == "/workflow" or cmd_name == "run_workflow":
                workflow = HyFI.workflow(**config)
                HyFI.run_workflow(workflow, dryrun=dryrun)
            elif "task" in config and (cmd_name is None or cmd_name == "run_task"):
                project = (
                    HyFI.init_project(**config["project"])
                    if "project" in config
                    else None
                )
                task = HyFI.task(**config["task"])
                HyFI.run_task(task, project=project, dryrun=dryrun)
            elif "runner" in config:
                runner = config["runner"]
                HyFI.run_intantiatable(runner, dryrun)
            elif "copier" in config and (cmd_name is None or cmd_name == "copy_conf"):
                copier_cfg = config["copier"]
                copier_cfg["dryrun"] = dryrun
                with Copier(**copier_cfg) as worker:
                    worker.run_copy()
            else:
                HyFI.about(**config.get("about", {}))

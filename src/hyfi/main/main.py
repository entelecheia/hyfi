"""
    This module contains the primary class for the hyfi config package, HyFI,
    as well as various utility functions and imports.
"""
import os
import random
from typing import Any, Callable, Dict, List, Optional, Union

import hydra
from omegaconf import DictConfig, OmegaConf

from hyfi.cached_path import cached_path
from hyfi.composer import GENERATOR, Composer, SpecialKeys
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
from hyfi.main import __project_root_path__, __project_workspace_path__, global_config
from hyfi.pipeline import PIPELINEs
from hyfi.pipeline.configs import PipeConfig
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.conf import CONFs
from hyfi.utils.datasets import DATASETs
from hyfi.utils.envs import ENVs
from hyfi.utils.funcs import FUNCs
from hyfi.utils.gpumon import GPUs
from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING
from hyfi.utils.notebooks import NBs
from hyfi.utils.packages import PKGs
from hyfi.workflow import WorkflowConfig

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
    CONFs,
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

    global_config = global_config
    global_hyfi = global_hyfi
    SpeicialKeys = SpecialKeys
    config_module = global_hyfi.config_module
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
        """
        global_hyfi.initialize(
            package_path=package_path,
            version=version,
            plugins=plugins,
            user_config_path=user_config_path,
            config_dirname=config_dirname,
        )

    @staticmethod
    def about(**args) -> None:
        """Print the about information"""
        global_config.print_about(**args)

    @staticmethod
    def init_project(
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
            **kwargs,
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
    def initialize(force: bool = False) -> None:
        """
        Initialize the global config.

        Args:
            force: If True, force initialization even if already initialized.

        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        global_config.initialize(force=force)

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
    def pipe(**kwargs) -> PipeConfig:
        """
        Return the PipeConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the PipeConfig constructor.

        Returns:
            PipeConfig: An instance of the PipeConfig class.
        """
        return PipeConfig(**kwargs)

    @staticmethod
    def task(**kwargs) -> TaskConfig:
        """
        Return the TaskConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the TaskConfig constructor.

        Returns:
            TaskConfig: An instance of the TaskConfig class.
        """
        if global_config.project and "project" in kwargs:
            del kwargs["project"]
        task = TaskConfig(**kwargs)
        if global_config.project:
            task.project = global_config.project
        return task

    @staticmethod
    def workflow(**kwargs) -> WorkflowConfig:
        """
        Return the WorkflowConfig.

        Args:
            **kwargs: Additional keyword arguments to pass to the WorkflowConfig constructor.

        Returns:
            WorkflowConfig: An instance of the WorkflowConfig class.
        """
        config_group = kwargs.get("_config_group_")
        config_name = kwargs.get("workflow_name")
        if config_group and config_group == "workflow" and config_name:
            cfg = HyFI.compose_as_dict(
                config_group=f"{config_group}={config_name}",
                config_data=kwargs,
                global_package=True,
            )
        else:
            cfg = kwargs
        if global_config.project and "project" in cfg:
            del cfg["project"]
        wf = WorkflowConfig(**cfg)
        if global_config.project:
            wf.project = global_config.project
        return wf

    @staticmethod
    def compose_as_dict(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        throw_on_compose_failure: bool = True,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Optional[str] = None,
        config_module: Optional[str] = None,
        global_package: bool = False,
        verbose: bool = False,
    ) -> Dict:
        """
        Compose a configuration by applying overrides and return the result as a dict(

        Args:
            config_group (Optional[str], optional): Name of the config group to compose (`config_group=name`). Defaults to None.
            overrides (Union[List[str], None], optional): List of config groups to apply overrides to (`overrides=["override_name"]`). Defaults to None.
            config_data (Union[Dict[str, Any], DictConfig, None], optional): Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`). Defaults to None.
            throw_on_compose_failure (bool, optional): If True throw an exception if composition fails. Defaults to True.
            throw_on_resolution_failure (bool, optional): If True throw an exception if resolution fails. Defaults to True.
            throw_on_missing (bool, optional): If True throw an exception if config_group doesn't exist. Defaults to False.
            root_config_name (Optional[str], optional): Name of the root config to be used (e.g. `hconf`). Defaults to None.
            config_module (Optional[str], optional): Name of the module containing the configuration. Defaults to None.
            global_package (bool, optional): If True, the configuration is loaded from the global package. Defaults to False.
            verbose (bool, optional): If True, print verbose output. Defaults to False.

        Returns:
            Dict: The composed configuration as a dictionary.
        """
        return Composer._compose_as_dict(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            throw_on_compose_failure=throw_on_compose_failure,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            config_name=root_config_name,
            config_module=config_module,
            global_package=global_package,
            verbose=verbose,
        )

    @staticmethod
    def compose(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        throw_on_compose_failure: bool = True,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Optional[str] = None,
        config_module: Optional[str] = None,
        global_package: bool = False,
        verbose: bool = False,
    ) -> DictConfig:
        """
        Compose a configuration by applying overrides

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`)
            return_as_dict: Return the result as a dict
            throw_on_compose_failure: If True throw an exception if composition fails
            throw_on_resolution_failure: If True throw an exception if resolution fails
            throw_on_missing: If True throw an exception if config_group doesn't exist
            root_config_name: Name of the root config to be used (e.g. `hconf`)
            config_module: Module of the config to be used (e.g. `hyfi.conf`)
            global_package: If True, the config assumed to be a global package
            verbose: If True print configuration to stdout

        Returns:
            A config object or a dictionary with the composed config
        """
        return Composer._compose(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            throw_on_compose_failure=throw_on_compose_failure,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            config_name=root_config_name,
            config_module=config_module,
            global_package=global_package,
            verbose=verbose,
        )

    @staticmethod
    def instantiate_config(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        global_package: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Instantiates an object using the provided config group and overrides

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`)
            global_package: If True, the config assumed to be a global package
            args: Optional positional parameters pass-through
            kwargs: Optional named parameters to override
                    parameters in the config object. Parameters not present
                    in the config objects are being passed as is to the target.
                    IMPORTANT: dataclasses instances in kwargs are interpreted as config
                                and cannot be used as passthrough

        Returns:
            if _target_ is a class name: the instantiated object
            if _target_ is a callable: the return value of the call
        """
        return Composer.instantiate_config(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            global_package=global_package,
            *args,
            **kwargs,
        )

    @staticmethod
    def print_config(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config_data: Optional[Union[Dict[str, Any], DictConfig]] = None,
        global_package: bool = False,
    ):
        """
        Print the configuration

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`)
            global_package: If True, the config assumed to be a global package
        """
        Composer.print_config(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            global_package=global_package,
        )

    @staticmethod
    def partial(
        config: Union[str, Dict],
        *args: Any,
        **kwargs: Any,
    ) -> Callable:
        return Composer.partial(config, *args, **kwargs)

    @staticmethod
    def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
        return Composer.instantiate(config, *args, **kwargs)

    @staticmethod
    def is_instantiatable(cfg: Any):
        return Composer.is_instantiatable(cfg)

    @staticmethod
    def getsource(obj):
        return Composer.getsource(obj)

    @staticmethod
    def viewsource(obj):
        return Composer.viewsource(obj)

    ###############################
    # Pipeline related functions
    ###############################
    @staticmethod
    def run(**cfg):
        """Run the provided config"""
        HyFI.run_config(config=cfg)

    @staticmethod
    def run_config(
        config_group: Optional[str] = None,
        overrides: Optional[List[str]] = None,
        config: Optional[Union[Dict[str, Any], DictConfig]] = None,
        global_package=False,
        **kwargs,
    ):
        """Run the config by composing it and running it"""
        if config_group:
            logger.info("Composing the HyFI config from config group %s", config_group)
            config = HyFI.compose_as_dict(
                config_group=config_group,
                overrides=overrides,
                config_data=config,
                global_package=global_package,
            )
        config = HyFI.to_dict(config) if config else {}
        if not isinstance(config, dict):
            raise ValueError("The config must be a dictionary")
        cmd_name = config.get("cmd_name")
        # Check if the config is instantiatable
        if HyFI.is_instantiatable(config):
            logger.info("Instantiating the HyFI config")
            task = HyFI.instantiate(config)
            if task and getattr(task, "__call__", None):
                logger.info("The HyFI config is callable, running it")
                task()
        else:
            logger.info(
                "The HyFI config is not instantiatable, running HyFI task with the config"
            )
            # Run the HyFI task
            config_group = config.get("_config_group_", "")
            if config_group == "workflow" or cmd_name == "run_workflow":
                workflow = HyFI.workflow(**config)
                HyFI.run_workflow(workflow)
            elif "task" in config and (cmd_name is None or cmd_name == "run_task"):
                project = (
                    HyFI.init_project(**config["project"])
                    if "project" in config
                    else None
                )
                task = HyFI.task(**config["task"])
                HyFI.run_task(task, project=project)
            elif "copier" in config and (cmd_name is None or cmd_name == "copy_conf"):
                with Copier(**config["copier"]) as worker:
                    worker.run_copy()
            else:
                HyFI.about(**config.get("about", {}))
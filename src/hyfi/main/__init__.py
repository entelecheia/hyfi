"""
    This module contains the primary class for the hyfi config package, HyFI,
    as well as various utility functions and imports.
"""
import os
import random
from typing import Any, Callable, Dict, List, Optional, Union

import hydra
from omegaconf import DictConfig, OmegaConf

from hyfi.about import __version__
from hyfi.cached_path import cached_path
from hyfi.composer import Composer, SpecialKeys
from hyfi.copier import Copier
from hyfi.core import __home_path__, __hyfi_path__
from hyfi.core.config import __global_config__, __search_package_path__
from hyfi.dotenv import DotEnvConfig
from hyfi.graphics import GRAPHICs
from hyfi.joblib import BATCHER, JobLibConfig
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
OmegaConf.register_new_resolver("__version__", __version__)
OmegaConf.register_new_resolver("__search_package_path__", __search_package_path__)
OmegaConf.register_new_resolver("__home_path__", __home_path__)
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
    GPUs,
    GRAPHICs,
    IOLIBs,
    LOGGING,
    NBs,
    PIPELINEs,
    PKGs,
):
    """Primary class for the hyfi config package"""

    config = __global_config__
    SpeicialKeys = SpecialKeys
    __version__ = __global_config__._version_
    __hyfi_path__ = __hyfi_path__()
    __home_path__ = __home_path__()

    def __init__(self) -> None:
        raise NotImplementedError("Use one of the static construction functions")

    @staticmethod
    def about(**args) -> None:
        """Print the about information"""
        __global_config__.print_about(**args)

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
        __global_config__.init_project(
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
        if __global_config__.project:
            return __global_config__.project
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
        __global_config__.project = project

    @staticmethod
    def initialize(force: bool = False) -> None:
        """
        Initialize the global config.

        Args:
            force: If True, force initialization even if already initialized.

        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        __global_config__.initialize(force=force)

    @staticmethod
    def terminate() -> None:
        """
        Terminate the global config.

        Returns:
            bool: True if termination was successful, False otherwise.
        """
        __global_config__.terminate()

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
        if __global_config__.project and "project" in kwargs:
            del kwargs["project"]
        task = TaskConfig(**kwargs)
        if __global_config__.project:
            task.project = __global_config__.project
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
        if _config_name_ := kwargs.get("_config_name_"):
            cfg = HyFI.compose_as_dict(
                config_group=f"workflow={_config_name_}",
                config_data=kwargs,
                global_package=True,
            )
        else:
            cfg = kwargs
        if __global_config__.project and "project" in cfg:
            del cfg["project"]
        wf = WorkflowConfig(**cfg)
        if __global_config__.project:
            wf.project = __global_config__.project
        return wf

    @staticmethod
    def compose_as_dict(
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        global_package: bool = False,
        verbose: bool = False,
    ) -> Dict:
        """
        Compose a configuration by applying overrides and return the result as a dict(

        Args:
            config_group (Union[str, None], optional): Name of the config group to compose (`config_group=name`). Defaults to None.
            overrides (Union[List[str], None], optional): List of config groups to apply overrides to (`overrides=["override_name"]`). Defaults to None.
            config_data (Union[Dict[str, Any], DictConfig, None], optional): Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`). Defaults to None.
            throw_on_resolution_failure (bool, optional): If True throw an exception if resolution fails. Defaults to True.
            throw_on_missing (bool, optional): If True throw an exception if config_group doesn't exist. Defaults to False.
            root_config_name (Union[str, None], optional): Name of the root config to be used (e.g. `hconf`). Defaults to None.
            config_module (Union[str, None], optional): Name of the module containing the configuration. Defaults to None.
            global_package (bool, optional): If True, the configuration is loaded from the global package. Defaults to False.
            verbose (bool, optional): If True, print verbose output. Defaults to False.

        Returns:
            Dict: The composed configuration as a dictionary.
        """
        return Composer._compose_as_dict(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            config_name=root_config_name,
            config_module=config_module,
            global_package=global_package,
            verbose=verbose,
        )

    @staticmethod
    def compose(
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
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
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            config_name=root_config_name,
            config_module=config_module,
            global_package=global_package,
            verbose=verbose,
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
    def run(cfg: Union[Dict, DictConfig], target: Optional[str] = None):
        """Run the config"""
        cfg = HyFI.to_dict(cfg)
        if "tasks" in cfg:
            workflow = HyFI.workflow(**cfg)
            HyFI.run_workflow(workflow)
        elif "task" in cfg and (target is None or target == "task"):
            project = HyFI.init_project(**cfg["project"]) if "project" in cfg else None
            task = HyFI.task(**cfg["task"])
            HyFI.run_task(task, project=project)
        elif "copier" in cfg and (target is None or target == "copier"):
            with Copier(**cfg["copier"]) as worker:
                worker.run_copy()
        else:
            if target and target not in cfg:
                logger.warning("Target %s not found in config", target)
            HyFI.about(**cfg.get("about", {}))

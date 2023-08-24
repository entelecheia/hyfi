from functools import reduce
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from hyfi.composer import BaseConfig, Composer
from hyfi.module import Module
from hyfi.path.task import TaskPath
from hyfi.pipeline.config import Pipeline, Pipelines, run_pipe
from hyfi.utils.contexts import change_directory, elapsed_timer
from hyfi.utils.logging import LOGGING
from hyfi.utils.packages import PKGs

logger = LOGGING.getLogger(__name__)


class Task(BaseConfig):
    _config_name_: str = "__init__"
    _config_group_: str = "/task"

    task_name: str = "demo-task"
    task_root: str = "workspace"
    version: str = "0.0.0"
    module: Optional[Module] = None
    path: TaskPath = TaskPath()
    pipelines: Optional[List[Union[str, Dict]]] = []

    _property_set_methods_ = {
        "task_name": "set_task_name",
        "task_root": "set_task_root",
    }

    def set_task_root(self, val: Union[str, Path]):
        if not self.task_root or self.task_root != val:
            self.path.task_root = str(val)

    def set_task_name(self, val):
        if not self.task_name or self.task_name != val:
            self.path.task_name = val

    @property
    def config(self):
        return self.model_dump()

    @property
    def root_dir(self) -> Path:
        return self.path.root_dir

    @property
    def task_dir(self) -> Path:
        return self.path.task_dir

    @property
    def project_dir(self) -> Path:
        return self.path.project_dir

    @property
    def workspace_dir(self) -> Path:
        return self.path.workspace_dir

    @property
    def output_dir(self) -> Path:
        return self.path.output_dir

    @property
    def model_dir(self) -> Path:
        return self.path.model_dir

    @property
    def log_dir(self) -> Path:
        return self.path.log_dir

    @property
    def cache_dir(self) -> Path:
        return self.path.cache_dir

    @property
    def library_dir(self) -> Path:
        return self.path.library_dir

    @property
    def dataset_dir(self):
        return self.path.dataset_dir

    def print_config(self):
        Composer.print(self.config)

    def load_modules(self):
        """Load the modules"""
        if not self.module:
            logger.info("No module to load")
            return
        if not self.module.modules:
            logger.info("No modules to load")
            return
        library_dir = self.library_dir
        for module in self.module.modules:
            name = module.name
            libname = module.libname
            liburi = module.liburi
            specname = module.specname
            libpath = library_dir / libname
            syspath = module.get("syspath")
            if syspath is not None:
                syspath = library_dir / syspath
            PKGs.ensure_import_module(name, libpath, liburi, specname, syspath)

    def reset(self, objects=None, release_gpu_memory=True):
        """Reset the memory cache"""
        if isinstance(objects, list):
            for obj in objects:
                del obj
        if release_gpu_memory:
            from hyfi.utils.gpumon import GPUMon

            GPUMon.release_gpu_memory()

    def get_pipelines(self) -> Pipelines:
        """
        Get the list of pipelines for a task

        Args:
            task: The task to get the pipelines for

        Returns:
            A list of PipelineConfig objects
        """
        self.pipelines = self.pipelines or []
        pipelines: Pipelines = []
        for name in self.pipelines:
            if isinstance(name, str) and isinstance(getattr(self, name), dict):
                pipeline = Pipeline(**getattr(self, name))
                if not pipeline.name:
                    pipeline.name = name
                pipelines.append(pipeline)
        return pipelines

    def run(
        self,
        pipelines: Optional[Pipelines] = None,
    ):
        """
        Run pipelines specified in the task

        Args:
            pipelines: The pipelines to run
        """
        # Run all pipelines in the task.
        pipelines = pipelines or self.get_pipelines()
        if self.verbose:
            logger.info("Running %s pipeline(s)", len(pipelines or []))
        with elapsed_timer(format_time=True) as elapsed:
            for pipeline in pipelines:
                if self.verbose:
                    logger.info("Running pipeline: %s", pipeline.name)
                initial_object = self if pipeline.use_task_as_initial_object else None
                self.run_pipeline(pipeline, initial_object)
            # Print the elapsed time.
            if self.verbose:
                logger.info(
                    " >> elapsed time for the task with %s pipelines: %s",
                    len(pipelines or []),
                    elapsed(),
                )

    def run_pipeline(
        self,
        pipeline: Union[Dict, Pipeline],
        initial_object: Optional[Any] = None,
    ) -> Any:
        """
        Run a pipeline given a config

        Args:
            config: PipelineConfig to run the pipeline
            initial_obj: Object to use as initial value
            task: TaskConfig to use as task

        Returns:
            The result of the pipeline
        """
        # If config is not a PipelineConfig object it will be converted to a PipelineConfig object.
        if not isinstance(pipeline, Pipeline):
            pipeline = Pipeline(**Composer.to_dict(pipeline))
        pipes = pipeline.get_pipes()
        if (
            initial_object is None
            and pipeline.initial_object is not None
            and Composer.is_instantiatable(pipeline.initial_object)
        ):
            initial_object = Composer.instantiate(pipeline.initial_object)
        # Return initial object for the initial object
        if not pipes:
            logger.warning("No pipes specified")
            return initial_object

        pipe_names = [pipe.run for pipe in pipes]
        logger.info("Applying %s pipes: %s", len(pipe_names), pipe_names)
        # Run the task in the current directory.
        if self is None:
            self = Task()
        with elapsed_timer(format_time=True) as elapsed:
            with change_directory(self.workspace_dir):
                rst = reduce(run_pipe, pipes, initial_object)
            # Print the elapsed time.
            if pipeline.verbose:
                logger.info(
                    " >> elapsed time for the pipeline with %s pipes: %s",
                    len(pipes),
                    elapsed(),
                )
        return rst

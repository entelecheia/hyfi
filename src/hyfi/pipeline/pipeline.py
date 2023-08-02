"""
A class to run a pipeline.
"""
from typing import Any, Dict, Optional, Union

from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING
from hyfi.workflow import WorkflowConfig

from .config import PipeConfig, PipelineConfig, Pipelines, get_running_configs, run_pipe

logger = LOGGING.getLogger(__name__)


class PIPELINEs:
    """
    A class to run a pipeline.
    """

    @staticmethod
    def run_pipeline(
        config: Union[Dict, PipelineConfig],
        initial_object: Optional[Any] = None,
        task: Optional[TaskConfig] = None,
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
        if task is None:
            task = TaskConfig()
        return task.run_pipeline(config, initial_object)
        # # If config is not a PipelineConfig object it will be converted to a PipelineConfig object.
        # if not isinstance(config, PipelineConfig):
        #     config = PipelineConfig(**Composer.to_dict(config))
        # pipes = config.get_pipes()
        # if (
        #     initial_object is None
        #     and config.initial_object is not None
        #     and Composer.is_instantiatable(config.initial_object)
        # ):
        #     initial_object = Composer.instantiate(config.initial_object)
        # # Return initial object for the initial object
        # if not pipes:
        #     logger.warning("No pipes specified")
        #     return initial_object

        # pipe_names = [pipe.run for pipe in pipes]
        # logger.info("Applying %s pipes: %s", len(pipe_names), pipe_names)
        # # Run the task in the current directory.
        # with elapsed_timer(format_time=True) as elapsed:
        #     with change_directory(task.workspace_dir):
        #         rst = reduce(PIPELINEs.run_pipe, pipes, initial_object)
        #     # Print the elapsed time.
        #     if config.verbose:
        #         logger.info(
        #             " >> elapsed time for the pipeline with %s pipes: %s",
        #             len(pipes),
        #             elapsed(),
        #         )
        # return rst

    @staticmethod
    def run_pipe(
        obj: Any,
        config: Union[Dict, PipeConfig],
    ) -> Any:
        """
        Run a pipe on an object

        Args:
            obj: The object to pipe on
            config: The configuration for the pipe

        Returns:
            The result of the pipe
        """
        return run_pipe(obj, config)

    #     # Create a PipeConfig object if not already a PipeConfig.
    #     if not isinstance(config, PipeConfig):
    #         config = PipeConfig(**Composer.to_dict(config))
    #     pipe_fn = config.get_pipe_func()
    #     # Return the object that is being used to execute the pipe function.
    #     if pipe_fn is None:
    #         logger.warning("No pipe function specified")
    #         return obj
    #     # Run a pipe with the pipe_fn
    #     if config.verbose:
    #         logger.info("Running a pipe with %s", config.pipe_target)
    #     # Apply pipe function to each object.
    #     if isinstance(obj, dict):
    #         objs = {}
    #         # Apply pipe to each object.
    #         for no, name in enumerate(obj):
    #             obj_ = obj[name]

    #             # Apply pipe to an object.
    #             if config.verbose:
    #                 logger.info(
    #                     "Applying pipe to an object [%s], %d/%d",
    #                     name,
    #                     no + 1,
    #                     len(obj),
    #                 )

    #             objs[name] = pipe_fn(obj_, config)
    #         return objs

    #     return pipe_fn(obj, config)

    # @staticmethod
    # def get_pipelines(task: TaskConfig) -> Pipelines:
    #     """
    #     Get the list of pipelines for a task

    #     Args:
    #         task: The task to get the pipelines for

    #     Returns:
    #         A list of PipelineConfig objects
    #     """
    #     task.pipelines = task.pipelines or []
    #     pipelines: Pipelines = []
    #     for name in task.pipelines:
    #         if isinstance(name, str) and isinstance(getattr(task, name), dict):
    #             pipeline = PipelineConfig(**getattr(task, name))
    #             if not pipeline.name:
    #                 pipeline.name = name
    #             pipelines.append(pipeline)
    #     return pipelines

    @staticmethod
    def run_task(task: TaskConfig, project: Optional[ProjectConfig] = None):
        """
        Run pipelines specified in the task

        Args:
            task: TaskConfig to run pipelines for
            project: ProjectConfig to run pipelines
        """
        task.run(project=project)

    @staticmethod
    def run_workflow(workflow: WorkflowConfig):
        """
        Run the tasks specified in the workflow

        Args:
            workflow: WorkflowConfig object to run
        """
        if workflow.verbose:
            logger.info("Running %s task(s)", len(workflow.tasks or []))
        # Run all tasks in the workflow.
        with elapsed_timer(format_time=True) as elapsed:
            for rc in get_running_configs(workflow.get_tasks()):
                task = workflow.get_running_task(rc)
                task_name = (
                    task.task_name
                    if isinstance(task, TaskConfig)
                    else getattr(task, "_config_name_", "unknown")
                )
                logger.info("Running task [%s] with [%s]", task_name, rc)
                if isinstance(task, TaskConfig):
                    # Run the task if verbose is true.
                    task.run(project=workflow.project)
                elif task is not None and getattr(task, "__call__", None):
                    if rc.run_kwargs:
                        task(**rc.run_kwargs)
                    else:
                        task()
                else:
                    logger.warning("Invalid task: %s", task)
            # Print the elapsed time.
            if workflow.verbose:
                logger.info(
                    " >> elapsed time for the workflow with %s tasks: %s",
                    len(workflow.tasks or []),
                    elapsed(),
                )
        # Run the pipelines in the workflow, if any.
        if workflow.pipelines:
            task = workflow.get_task()
            logger.info(
                "Running pipelines in the workflow with task [%s]", task.task_name
            )
            with elapsed_timer(format_time=True) as elapsed:
                for pipeline in PIPELINEs.get_worflow_pipelines(workflow):
                    if task.verbose:
                        logger.info("Running pipeline: %s", pipeline.name)
                    initial_object = (
                        task if pipeline.use_task_as_initial_object else None
                    )
                    task.run(pipeline, initial_object)
                # Print the elapsed time.
                if workflow.verbose:
                    logger.info(
                        " >> elapsed time for the workflow with %s pipelines: %s",
                        len(task.pipelines or []),
                        elapsed(),
                    )

    @staticmethod
    def get_worflow_pipelines(workflow: WorkflowConfig) -> Pipelines:
        """
        Get the list of pipelines for a workflow

        Args:
            task: The task to get the pipelines for

        Returns:
            A list of PipelineConfig objects
        """
        workflow.pipelines = workflow.pipelines or []
        pipelines: Pipelines = []
        for name in workflow.pipelines:
            if isinstance(name, str) and isinstance(getattr(workflow, name), dict):
                pipeline = PipelineConfig(**getattr(workflow, name))
                if not pipeline.name:
                    pipeline.name = name
                pipelines.append(pipeline)
        return pipelines

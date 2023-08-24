from typing import Any, Dict, List, Optional, Union

from hyfi.composer import BaseModel, Composer, model_validator
from hyfi.pipeline.config import (
    Pipeline,
    Pipelines,
    Running,
    RunningTasks,
    get_running_configs,
)
from hyfi.project import Project
from hyfi.task import Task
from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

Tasks = List[Any]


class Workflow(BaseModel):
    _config_group_: str = "/workflow"
    _config_name_: str = "__init__"
    _auto_populate_: bool = True

    workflow_name: str = _config_name_
    project: Optional[Project] = None
    task: Optional[Task] = None
    tasks: Optional[List[Union[str, Dict]]] = []
    pipelines: Optional[List[Union[str, Dict]]] = []
    verbose: bool = False

    @model_validator(mode="before")
    def validate_model_config_before(cls, data):
        # logger.debug("Validating model config before validating each field.")
        return Composer.to_dict(data)

    def get_running_tasks(self) -> RunningTasks:
        return get_running_configs(self.tasks or [])

    def get_running_task(self, rc: Running) -> Any:
        config = getattr(self, rc.uses, None)
        if rc.uses and isinstance(config, dict):
            if Composer.is_instantiatable(config):
                task = Composer.instantiate(config)
                if task is not None and getattr(task, "__call__", None):
                    return task
            else:
                task = Task(**config)
                task.name = rc.uses
                return task
        return None

    def get_task(self):
        return self.task or Task()

    def run(self):
        """
        Run the tasks specified in the workflow
        """
        if self.verbose:
            logger.info("Running %s task(s)", len(self.tasks or []))
        # Run all tasks in the workflow.
        with elapsed_timer(format_time=True) as elapsed:
            for rc in self.get_running_tasks():
                task = self.get_running_task(rc)
                task_name = (
                    task.task_name
                    if isinstance(task, Task)
                    else getattr(task, "_config_name_", "unknown")
                )
                logger.info("Running task [%s] with [%s]", task_name, rc)
                if isinstance(task, Task):
                    # Run the task if verbose is true.
                    task.run()
                elif task is not None and getattr(task, "__call__", None):
                    if rc.run_kwargs:
                        task(**rc.run_kwargs)
                    else:
                        task()
                else:
                    logger.warning("Invalid task: %s", task)
            # Print the elapsed time.
            if self.verbose:
                logger.info(
                    " >> elapsed time for the workflow with %s tasks: %s",
                    len(self.tasks or []),
                    elapsed(),
                )
        # Run the pipelines in the workflow, if any.
        if self.pipelines:
            task = self.get_task()
            logger.info(
                "Running pipelines in the workflow with task [%s]", task.task_name
            )
            task.run(
                pipelines=self.get_pipelines(),
            )

    def get_pipelines(self) -> Pipelines:
        """
        Get the list of pipelines for a workflow

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

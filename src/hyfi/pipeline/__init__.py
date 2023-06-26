"""
A class to run a pipeline.
"""
from functools import reduce
from typing import Any, Dict, List, Optional, Union

from pydantic import validator

from hyfi.composer import Composer
from hyfi.pipeline.configs import BaseRunConfig, PipeConfig, Pipes, RunningConfig
from hyfi.task import TaskConfig
from hyfi.utils.contexts import change_directory
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class PipelineConfig(BaseRunConfig):
    """Pipeline Configuration"""

    steps: Optional[List[Union[str, Dict]]] = []

    @validator("steps", pre=True)
    def steps_to_list(cls, v):
        return [v] if isinstance(v, str) else Composer.to_dict(v)

    def update_configs(
        self,
        rc: Union[Dict, RunningConfig],
    ):
        if isinstance(rc, dict):
            rc = RunningConfig(**rc)
        self.name = rc.name or self.name
        self.desc = rc.desc or self.desc

    def get_pipes(self, task: Optional[TaskConfig] = None) -> Pipes:
        pipes: Pipes = []
        for rc in PIPELINEs.get_RCs(self.steps):
            if rc.uses in self.__dict__ and isinstance(self.__dict__[rc.uses], dict):
                config = self.__dict__[rc.uses]
                pipe = PipeConfig(**Composer.update(config, rc.dict()))
                if task is not None:
                    pipe.task = task
                pipes.append(pipe)
        return pipes


Pipelines = List[PipelineConfig]


class PIPELINEs:
    """
    A class to run a pipeline.
    """

    @staticmethod
    def run_pipeline(
        config: Union[Dict, PipelineConfig],
        initial_obj: Optional[Any] = None,
        task: Optional[TaskConfig] = None,
    ) -> Any:
        if not isinstance(config, PipelineConfig):
            config = PipelineConfig(**Composer.to_dict(config))
        pipes = config.get_pipes(task)
        if not pipes:
            logger.warning("No pipes specified")
            return initial_obj

        logger.info("Applying %s pipes", len(pipes))
        if task is not None:
            with change_directory(task.root_dir):
                return reduce(PIPELINEs.run_pipe, pipes, initial_obj)
        return reduce(PIPELINEs.run_pipe, pipes, initial_obj)

    @staticmethod
    def run_pipe(
        obj: Any,
        config: Union[Dict, PipeConfig],
    ) -> Any:
        if not isinstance(config, PipeConfig):
            config = PipeConfig(**Composer.to_dict(config))
        config.run.task = config.task
        pipe_fn = config.get_func()
        if pipe_fn is None:
            logger.warning("No pipe function specified")
            return obj
        if config.verbose:
            logger.info("Running a pipe with %s", pipe_fn)
        if isinstance(obj, dict):
            objs = {}
            for no, name in enumerate(obj):
                obj_ = obj[name]

                if config.verbose:
                    logger.info(
                        "Applying pipe to an object [%s], %d/%d",
                        name,
                        no + 1,
                        len(obj),
                    )

                objs[name] = pipe_fn(obj_, config.run)
            return objs

        return pipe_fn(obj, config.run)

    @staticmethod
    def get_RCs(config_list: list) -> List[RunningConfig]:
        RCs: List[RunningConfig] = []
        if not config_list:
            logger.warning("No running configs provided")
            return RCs
        for rc in config_list:
            if isinstance(rc, str):
                RCs.append(RunningConfig(uses=rc))
            elif isinstance(rc, dict):
                RCs.append(RunningConfig(**rc))
            else:
                raise ValueError(f"Invalid running config: {rc}")
        return RCs

    @staticmethod
    def get_pipelines(task: TaskConfig) -> Pipelines:
        task.pipelines = task.pipelines or []
        pipelines: Pipelines = [
            PipelineConfig(**task.__dict__[name])
            for name in task.pipelines
            if name in task.__dict__ and isinstance(task.__dict__[name], dict)
        ]
        return pipelines

    @staticmethod
    def run_task_pipelines(task: TaskConfig):
        """Run the pipelines specified in the task"""
        for pipeline in PIPELINEs.get_pipelines(task):
            if task.verbose:
                logger.info("Running pipeline: %s", pipeline.dict())
            PIPELINEs.run_pipeline(pipeline, task=task)

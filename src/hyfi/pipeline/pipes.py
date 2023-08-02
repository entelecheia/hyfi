"""
    Configuration for HyFi Pipelines
"""
from typing import Any, Callable, Dict, List, Optional, Union

from hyfi.composer import Composer, model_validator
from hyfi.task import TaskConfig
from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING

from .base import BaseRunConfig

logger = LOGGING.getLogger(__name__)


class PipeConfig(BaseRunConfig):
    """Pipe Configuration"""

    pipe_target: str = ""
    name: Optional[str] = ""
    desc: Optional[str] = ""
    env: Optional[Dict[str, Any]] = {}
    use_pipe_obj: bool = True
    pipe_obj_arg_name: Optional[str] = ""
    return_pipe_obj: bool = False
    task: Optional[TaskConfig] = None

    def set_enviroment(self):
        if self.env:
            ENVs.check_and_set_osenv_vars(self.env)

    def get_pipe_func(self) -> Optional[Callable]:
        if self.pipe_target.startswith("lambda"):
            return eval(self.pipe_target)
        elif self.pipe_target:
            return Composer.partial(self.pipe_target)
        else:
            return None

    def get_run_func(self) -> Optional[Callable]:
        run_cfg = self.run_config
        run_target = self.run_target
        if run_target and run_target.startswith("lambda"):
            logger.info("Returning lambda function: %s", run_target)
            return eval(run_target)
        elif run_cfg:
            if self.pipe_obj_arg_name:
                run_cfg.pop(self.pipe_obj_arg_name)
            logger.info(
                "Returning partial function: %s with kwargs: %s", run_target, run_cfg
            )
            return Composer.partial(run_cfg)
        else:
            logger.warning("No function found for %s", self)
            return None
        # if self.run.startswith("lambda"):
        #     logger.info("Returning lambda function: %s", self.run)
        #     return eval(self.run)
        # elif self.run:
        #     kwargs = self.run_with or {}
        #     if self.pipe_obj_arg_name:
        #         kwargs.pop(self.pipe_obj_arg_name)
        #     logger.info(
        #         "Returning partial function: %s with kwargs: %s", self.run, kwargs
        #     )
        #     return Composer.partial(self.run, **kwargs)
        # else:
        #     logger.warning("No function found for %s", self)
        #     return None


class DataframePipeConfig(PipeConfig):
    columns_to_apply: Optional[Union[str, List[str]]] = []
    use_batcher: bool = True
    num_workers: int = 1

    @model_validator(mode="before")
    def _check_and_set_values(cls, data):
        num_workers = data.get("num_workers")
        if num_workers and num_workers > 1:
            data["use_batcher"] = True
        return data

    @property
    def columns(self) -> List[str]:
        if not self.columns_to_apply:
            return []
        return (
            [self.columns_to_apply]
            if isinstance(self.columns_to_apply, str)
            else self.columns_to_apply
        )


Pipes = List[PipeConfig]

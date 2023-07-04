"""
    Configuration for HyFi Pipelines
"""
from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, model_validator

from hyfi.composer import Composer
from hyfi.composer.extended import XC
from hyfi.task import TaskConfig
from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BaseRunConfig(BaseModel):
    """Run Configuration"""

    run_with: Optional[Dict[str, Any]] = {}

    name: Optional[str] = ""
    desc: Optional[str] = ""
    env: Optional[Dict[str, Any]] = {}
    verbose: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=True,
        alias_generator=Composer.generate_alias_for_special_keys,
    )  # type: ignore

    def __init__(self, **config_kwargs):
        config_kwargs = Composer.replace_special_keys(config_kwargs)
        super().__init__(**config_kwargs)

    @property
    def kwargs(self):
        return self.run_with or {}


class RunningConfig(BaseRunConfig):
    """Running Configuration"""

    uses: str = ""


Steps = List[RunningConfig]
Pipelines = List[RunningConfig]
Tasks = List[RunningConfig]


class PipeConfig(BaseRunConfig):
    """Pipe Configuration"""

    pipe_target: str = ""
    run: str = ""

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
            return XC.partial(self.pipe_target)
        else:
            return None

    def get_run_func(self) -> Optional[Callable]:
        if self.run.startswith("lambda"):
            return eval(self.run)
        elif self.run:
            kwargs = self.run_with or {}
            if self.pipe_obj_arg_name:
                kwargs.pop(self.pipe_obj_arg_name)
            return XC.partial(self.run, **kwargs)
        else:
            return None


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

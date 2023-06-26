"""
    Configuration for HyFi Pipelines
"""
from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, root_validator

from hyfi.composer import Composer
from hyfi.composer.extended import XC
from hyfi.utils.envs import ENVs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BaseRunConfig(BaseModel):
    """Run Configuration"""

    _with_: Dict[str, Any] = {}

    name: Optional[str] = ""
    desc: Optional[str] = ""
    env: Optional[Dict[str, Any]] = {}
    verbose: bool = False

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
        validate_assignment = True
        exclude = {}
        include = {}
        underscore_attrs_are_private = False

    def __init__(self, **config_kwargs):
        config_kwargs = Composer.to_dict(config_kwargs)
        config_kwargs = Composer.replace_keys(config_kwargs, "with", "_with_")
        super().__init__(**config_kwargs)

    @property
    def kwargs(self):
        return self._with_ or {}


class RunningConfig(BaseRunConfig):
    """Running Configuration"""

    uses: str = ""


Steps = List[RunningConfig]
Pipelines = List[RunningConfig]
Tasks = List[RunningConfig]


class RunConfig(BaseRunConfig):
    """Run Configuration"""

    _target_: str = ""

    def set_enviroment(self):
        if self.env:
            ENVs.check_and_set_osenv_vars(self.env)

    def get_func(self) -> Optional[Callable]:
        if self._target_.startswith("lambda"):
            return eval(self._target_)
        elif self._target_:
            return XC.partial(self._target_, **self._with_ or {})
        else:
            return None


class DataframeRunConfig(RunConfig):
    columns_to_apply: Optional[Union[str, List[str]]] = []
    use_batcher: bool = True
    num_workers: int = 1

    @root_validator()
    def _check_and_set_values(cls, values):
        num_workers = values.get("num_workers")
        if num_workers and num_workers > 1:
            values["use_batcher"] = True
        return values

    @property
    def columns(self) -> List[str]:
        if not self.columns_to_apply:
            return []
        return (
            [self.columns_to_apply]
            if isinstance(self.columns_to_apply, str)
            else self.columns_to_apply
        )


class PipeConfig(RunConfig):
    """Pipe Configuration"""

    run: RunConfig = RunConfig()


Pipes = List[PipeConfig]

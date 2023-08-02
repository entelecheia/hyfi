"""
    Configuration for HyFi Pipelines
"""
from typing import Any, Dict, List, Optional, Union

from hyfi.composer import BaseModel, Composer, ConfigDict, model_validator
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BaseRunConfig(BaseModel):
    """Run Configuration"""

    run: Optional[Union[str, Dict[str, Any]]] = {}
    verbose: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=False,
        alias_generator=Composer.generate_alias_for_special_keys,
    )  # type: ignore

    @model_validator(mode="before")
    def validate_model_config_before(cls, data):
        # logger.debug("Validating model config before validating each field.")
        return Composer.replace_special_keys(Composer.to_dict(data))

    @property
    def run_config(self) -> Dict[str, Any]:
        if self.run and isinstance(self.run, str):
            return {"_target_": self.run}
        return self.run or {}

    @property
    def run_target(self) -> str:
        return self.run_config.get("_target_") or ""

    @property
    def run_kwargs(self) -> Dict[str, Any]:
        _kwargs = self.run_config.copy()
        _kwargs.pop("_target_", None)
        _kwargs.pop("_partial_", None)
        return _kwargs


class RunningConfig(BaseRunConfig):
    """Running Configuration"""

    uses: str = ""


Steps = List[RunningConfig]
Pipelines = List[RunningConfig]
Tasks = List[RunningConfig]
Calls = List[RunningConfig]

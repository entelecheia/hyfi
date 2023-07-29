from typing import Any, Dict, List, Optional, Union

from hyfi.composer import BaseModel, Composer, ConfigDict, model_validator
from hyfi.pipeline.configs import RunningConfig
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

Tasks = List[Any]


class WorkflowConfig(BaseModel):
    _config_group_: str = "workflow"
    _config_name_: str = "__init__"

    workflow_name: str = _config_name_
    project: Optional[ProjectConfig] = None
    tasks: Optional[List[Union[str, Dict]]] = []
    verbose: bool = False

    @model_validator(mode="before")
    def validate_model_config_before(cls, data):
        # logger.debug("Validating model config before validating each field.")
        return Composer.to_dict(data)

    def get_tasks(self) -> Tasks:
        return self.tasks or []

    def get_task(self, rc: RunningConfig) -> Any:
        config = getattr(self, rc.uses, None)
        if rc.uses and isinstance(config, dict):
            if Composer.is_instantiatable(config):
                task = Composer.instantiate(config)
                if task is not None and getattr(task, "__call__", None):
                    return task
            else:
                task = TaskConfig(**config)
                task.name = rc.uses
                return task
        return None

from typing import Any, Dict, List, Optional, Union

from hyfi.composer import BaseModel, Composer, ConfigDict, model_validator
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

Tasks = List[Any]


class WorkflowConfig(BaseModel):
    project: Optional[ProjectConfig] = None
    tasks: Optional[List[Union[str, Dict]]] = []
    verbose: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=False,
    )  # type: ignore

    @model_validator(mode="before")
    def validate_model_config_before(cls, data):
        # logger.debug("Validating model config before validating each field.")
        return Composer.to_dict(data)

    def get_tasks(self) -> Tasks:
        self.tasks = self.tasks or []
        tasks: Tasks = []
        for name in self.tasks:
            cfg = getattr(self, name, None)
            if isinstance(name, str) and isinstance(cfg, dict):
                if Composer.is_instantiatable(cfg):
                    task = Composer.instantiate(cfg)
                    if task is not None and getattr(task, "__call__", None):
                        tasks.append(task)
                else:
                    task = TaskConfig(**cfg)
                    task.name = name
                    tasks.append(task)
        return tasks

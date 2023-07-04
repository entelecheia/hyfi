from typing import Dict, List, Optional, Union

from hyfi.composer import BaseConfig
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

Tasks = List[TaskConfig]


class WorkflowConfig(BaseConfig):
    _config_name_: str = "__init__"
    _config_group_: str = "workflow"

    project: Optional[ProjectConfig] = None
    tasks: Optional[List[Union[str, Dict]]] = []

    def get_tasks(self) -> Tasks:
        self.tasks = self.tasks or []

        tasks: Tasks = [
            TaskConfig(**getattr(self, name))
            for name in self.tasks
            if isinstance(name, str) and isinstance(getattr(self, name), dict)
        ]
        return tasks

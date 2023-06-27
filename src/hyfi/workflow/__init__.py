from typing import Dict, List, Optional, Union

from hyfi.composer import BaseConfig
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

Tasks = List[TaskConfig]


class WorkflowConfig(BaseConfig):
    config_name: str = "__init__"
    config_group: str = "workflow"

    project: Optional[ProjectConfig] = None
    tasks: Optional[List[Union[str, Dict]]] = []

    def initialize_configs(self, **config_kwargs):
        super().initialize_configs(**config_kwargs)
        if "project" in self.__dict__ and self.__dict__["project"]:
            self.project = ProjectConfig.parse_obj(self.__dict__["project"])

    def get_tasks(self) -> TaskConfig:
        self.tasks = self.tasks or []
        tasks: TaskConfig = [
            TaskConfig(**self.__dict__[name])
            for name in self.tasks
            if name in self.__dict__ and isinstance(self.__dict__[name], dict)
        ]
        return tasks

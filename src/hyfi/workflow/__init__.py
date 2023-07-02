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

    # def initialize_configs(self, **config_kwargs):
    #     super().initialize_configs(**config_kwargs)
    #     subconfigs = {
    #         "project": ProjectConfig,
    #     }
    #     self.initialize_subconfigs(subconfigs, **config_kwargs)

    def get_tasks(self) -> Tasks:
        self.tasks = self.tasks or []
        config = self.__dict__
        tasks: Tasks = [
            TaskConfig(**config[name])
            for name in self.tasks
            if name in config and isinstance(config[name], dict)
        ]
        return tasks

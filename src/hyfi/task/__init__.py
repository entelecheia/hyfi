from pathlib import Path
from typing import Dict, List, Optional, Union

from hyfi.composer import BaseConfig, Composer
from hyfi.module import ModuleConfig
from hyfi.path.batch import BatchPathConfig
from hyfi.project import ProjectConfig
from hyfi.utils.logging import LOGGING
from hyfi.utils.packages import PKGs

logger = LOGGING.getLogger(__name__)


class TaskConfig(BaseConfig):
    _config_name_: str = "__init__"
    _config_group_: str = "task"

    task_name: str = "demo-task"
    task_root: str = "tmp/task"
    autoload: bool = False
    version: str = "0.0.0"
    module: Optional[ModuleConfig] = None
    path: Optional[BatchPathConfig] = None
    project: Optional[ProjectConfig] = None
    pipelines: Optional[List[Union[str, Dict]]] = []

    class Config:
        exclude = {
            "__data__",
            "project",
        }
        include = {}
        property_set_methods = {
            "task_name": "set_task_name",
            "task_root": "set_task_root",
            "project": "set_project",
        }

    def set_task_root(self, val: Union[str, Path]):
        if not self.task_root or self.task_root != val:
            self.initialize_configs(task_root=val)

    def set_task_name(self, val):
        print("set_task_name: ", val, "self.task_name: ", self.task_name)
        if not self.task_name or self.task_name != val:
            self.initialize_configs(task_name=val)

    def set_project(self, val):
        if isinstance(val, ProjectConfig):
            self.task_root = str(val.project_workspace_dir / self.task_name)

    def initialize_configs(self, **config_kwargs):
        super().initialize_configs(**config_kwargs)
        if "module" in self.__dict__ and self.__dict__["module"]:
            self.module = ModuleConfig.parse_obj(self.__dict__["module"])
        if "path" in self.__dict__ and self.__dict__["path"]:
            self.path = BatchPathConfig.parse_obj(self.__dict__["path"])

    @property
    def config(self):
        return self.dict()

    @property
    def root_dir(self) -> Path:
        return self.path.root_dir

    @property
    def output_dir(self) -> Path:
        return self.path.output_dir

    @property
    def project_name(self) -> str:
        return (
            self.project.project_name if self.project else f"{self.task_name}-project"
        )

    @property
    def project_dir(self) -> Path:
        return Path(self.project.project_root) if self.project else self.root_dir

    @property
    def workspace_dir(self) -> Path:
        return (
            Path(self.project.project_workspace_dir) if self.project else self.root_dir
        )

    @property
    def model_dir(self) -> Path:
        return self.path.model_dir

    @property
    def log_dir(self) -> Path:
        return self.project.path.log_dir if self.project else self.path.log_dir

    @property
    def cache_dir(self) -> Path:
        return self.project.path.cache_dir if self.project else self.path.cache_dir

    @property
    def library_dir(self) -> Path:
        return self.path.library_dir

    @property
    def verbose(self) -> bool:
        return bool(self.project.verbose) if self.project else False

    def print_config(self):
        Composer.print(self.config)

    def load_modules(self):
        """Load the modules"""
        if not self.module.modules:
            logger.info("No modules to load")
            return
        library_dir = self.library_dir
        for module in self.module.modules:
            name = module.name
            libname = module.libname
            liburi = module.liburi
            specname = module.specname
            libpath = library_dir / libname
            syspath = module.get("syspath")
            if syspath is not None:
                syspath = library_dir / syspath
            PKGs.ensure_import_module(name, libpath, liburi, specname, syspath)

    def reset(self, objects=None, release_gpu_memory=True):
        """Reset the memory cache"""
        if isinstance(objects, list):
            for obj in objects:
                del obj
        if release_gpu_memory:
            from hyfi.utils.gpumon import GPUMon

            GPUMon.release_gpu_memory()

import contextlib
from pathlib import Path
from typing import Union

from omegaconf import DictConfig
from pydantic import BaseModel

from hyfi.hydra import Composer
from hyfi.module import ModuleConfig
from hyfi.path.batch import BatchPathConfig
from hyfi.project import ProjectConfig
from hyfi.utils.lib import ensure_import_module
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


class TaskConfig(BaseModel):
    config_name: str = "__init__"
    config_group: str = "task"
    task_name: str
    path: BatchPathConfig = None  # type: ignore
    project: ProjectConfig = None  # type: ignore
    module: ModuleConfig = None  # type: ignore
    autoload: bool = False
    version: str = "0.0.0"
    _config_: DictConfig = None  # type: ignore
    _initial_config_: DictConfig = None  # type: ignore

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"
        validate_assignment = False
        exclude = {
            "_config_",
            "_initial_config_",
            "__data__",
            "path",
            "module",
            "project",
        }
        include = {}
        underscore_attrs_are_private = True
        property_set_methods = {
            "name": "set_name",
            "root_dir": "set_root_dir",
        }

    def __init__(
        self,
        config_name: str = "",
        config_group: str = "",
        root_dir: str = "",
        **args,
    ):
        if config_group:
            args = Composer.merge(Composer._compose(config_group), args)
        else:
            args = Composer.to_config(args)
        super().__init__(config_name=config_name, config_group=config_group, **args)

        object.__setattr__(self, "_config_", args)
        object.__setattr__(self, "_initial_config_", args.copy())
        self.initialize_configs(root_dir=root_dir)

    def __setattr__(self, key, val):
        super().__setattr__(key, val)
        method = self.__config__.property_set_methods.get(key)
        if method is not None:
            getattr(self, method)(val)

    def set_root_dir(self, root_dir: Union[str, Path]):
        path = self.config.path
        if path is None:
            path = Composer._compose("path=_batch_")
            logger.info(
                f"There is no path in the config, using default path: {path.root}"
            )
            self._config_.path = path
        if root_dir is not None:
            path.root = str(root_dir)
        self.path = BatchPathConfig(**path)

    def set_name(self, val):
        self._config_.name = val
        if self.task_name is None or self.task_name != val:
            self.task_name = val

    def initialize_configs(self, root_dir=None, **kwargs):
        self.root_dir = root_dir

    @property
    def config(self):
        return self._config_

    @property
    def root_dir(self) -> Path:
        return Path(self.path.root)

    @property
    def output_dir(self):
        return self.path.output_dir

    @property
    def project_name(self):
        return self.project.project_name

    @property
    def project_dir(self):
        return Path(self.project.project_dir)

    @property
    def workspace_dir(self):
        return Path(self.project.project_workspace_dir)

    @property
    def model_dir(self):
        return self.path.model_dir

    @property
    def log_dir(self):
        return self.project.path.log_dir

    @property
    def cache_dir(self):
        cache_dir = Path(self.project.path.global_cache)
        if cache_dir is None:
            cache_dir = self.output_dir / ".cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
        return Path(cache_dir)

    @property
    def library_dir(self):
        return self.path.library_dir

    @property
    def verbose(self):
        return self.project.verbose

    def autorun(self):
        return Composer.methods(self.auto, self)

    def show_config(self):
        Composer.print(self.dict())

    def load_modules(self):
        """Load the modules"""
        if self.module.get("modules") is None:
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
            ensure_import_module(name, libpath, liburi, specname, syspath)

    def reset(self, objects=None):
        """Reset the memory cache"""
        if isinstance(objects, list):
            for obj in objects:
                del obj
        with contextlib.suppress(ImportError):
            from hyfi.utils.gpu import GPUMon

            GPUMon.release_gpu_memory()

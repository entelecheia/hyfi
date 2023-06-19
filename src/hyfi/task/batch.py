from typing import Dict, List, Union

from omegaconf import DictConfig

from hyfi.batch import BatchConfig
from hyfi.hydra.main import XC
from hyfi.task import TaskConfig
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


class BatchTaskConfig(TaskConfig):
    batch_name: str = "demo"
    batch: BatchConfig = None  # type: ignore

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
            "task_name": "set_task_name",
            "task_root": "set_task_root",
            "batch_name": "set_batch_name",
            "batch_num": "set_batch_num",
        }

    def __init__(self, **args):
        super().__init__(**args)

    def set_batch_name(self, val):
        self.initialize_configs(batch_name=val)

    def set_batch_num(self, val):
        self.batch.batch_num = val

    def initialize_configs(
        self,
        config_name: str = "__batch__",
        config_group: str = "task",
        batch_config_class=BatchConfig,
        **data,
    ):
        super().initialize_configs(
            config_name=config_name,
            config_group=config_group,
            **data,
        )

        self.batch = batch_config_class(**self.__dict__["batch"])
        self.batch_num = self.batch.batch_num  # type: ignore
        # if self.project.use_huggingface_hub:
        #     self.secrets.init_huggingface_hub()
        if self.verbose:
            logger.info(
                "Initalized batch: %s(%s) in %s",
                self.batch_name,
                self.batch_num,
                self.root_dir,
            )

    @property
    def batch_num(self):
        return self.batch.batch_num

    @property
    def seed(self):
        return self.batch.seed

    @property
    def batch_dir(self):
        return self.batch.batch_dir

    @property
    def dataset_dir(self):
        return self.path.dataset_dir

    @property
    def verbose(self):
        return self.batch.verbose

    @property
    def device(self):
        return self.batch.device

    @property
    def num_devices(self):
        return self.batch.num_devices

    def save_config(
        self,
        config: Union[DictConfig, Dict, None] = None,
        exclude: Union[str, List[str], None] = None,
        include: Union[str, List[str], None] = None,
    ):
        """Save the batch config"""
        if not config:
            config = self.__dict__
        logger.info(
            "Saving config to %s",
            self.batch.config_filepath,
        )
        cfg = XC.to_dict(config)
        if not exclude:
            exclude = self.__config__.exclude  # type: ignore

        if include:
            if isinstance(include, str):
                include = [include]
            config_to_save = {key: cfg[key] for key in include}
        else:
            config_to_save = cfg
            if exclude:
                if isinstance(exclude, str):
                    exclude = [exclude]
                for key in exclude:
                    config_to_save.pop(key, None)
        XC.save(config_to_save, self.batch.config_filepath)
        self.save_settings(exclude=exclude)
        return self.batch.config_filename

    def save_settings(self, exclude=None, exclude_none=True):
        def dumper(obj):
            return XC.to_dict(obj) if isinstance(obj, DictConfig) else str(obj)

        if exclude is None:
            exclude = self.__config__.exclude  # type: ignore
        config = self.dict(exclude=exclude, exclude_none=exclude_none)
        if self.verbose:
            logger.info(
                "Saving config to %s",
                self.batch.config_jsonpath,
            )
        XC.save_json(config, self.batch.config_jsonpath, default=dumper)

    def load_config(
        self,
        batch_name: str = "",
        batch_num: int = -1,
        **data,
    ):
        """Load the config from the batch config file"""
        if self.verbose:
            logger.info(
                "> Loading config for batch_name: %s batch_num: %s",
                batch_name,
                batch_num,
            )
        if not batch_name:
            batch_name = self.batch_name

        if batch_num is None:
            batch_num = -1
        cfg = self.__dict__.copy()
        if batch_num >= 0:
            batch = BatchConfig(batch_name=batch_name, batch_num=batch_num)
            _path = batch.config_filepath
            if _path.is_file():
                logger.info("Loading config from %s", _path)
                batch_cfg = XC.load(_path)
                logger.info("Merging config with the loaded config")
                cfg = XC.merge(cfg, batch_cfg)
            else:
                logger.info("No config file found at %s", _path)
                batch_num = -1
        if self.verbose:
            logger.info("Merging config with args: %s", data)
        cfg = XC.to_dict(XC.merge(cfg, data))

        self.initialize_configs(**cfg)

        return self.config

    def print_config(
        self,
        batch_name: str = "",
        batch_num: int = -1,
    ):
        self.load_config(batch_name, batch_num)
        XC.print(self.dict())
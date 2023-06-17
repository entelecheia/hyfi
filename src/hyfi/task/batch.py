from omegaconf import DictConfig

from hyfi.batch import BatchConfig
from hyfi.hydra.main import XC
from hyfi.task import TaskConfig
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


class BatchTaskConfig(TaskConfig):
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
            "secret",
            "auto",
            "project",
        }
        include = {}
        underscore_attrs_are_private = True
        property_set_methods = {
            "name": "set_name",
            "batch_name": "set_name",
            "batch_num": "set_batch_num",
            "root_dir": "set_root_dir",
        }

    def __init__(self, **args):
        super().__init__(**args)

    def set_name(self, val):
        super().set_name(val)
        self._config_.batch.batch_name = val
        self.batch.batch_name = val
        self.initialize_configs(name=val)

    def set_batch_num(self, val):
        self._config_.batch.batch_num = val
        self.batch.batch_num = val

    def initialize_configs(
        self, root_dir=None, batch_config_class=BatchConfig, **kwargs
    ):
        super().initialize_configs(root_dir=root_dir, **kwargs)

        self.batch = batch_config_class(**self.config.batch)
        self.batch_num = self.batch.batch_num
        # if self.project.use_huggingface_hub:
        #     self.secrets.init_huggingface_hub()
        if self.verbose:
            logger.info(
                f"Initalized batch: {self.batch_name}({self.batch_num}) in {self.root_dir}"
            )

    @property
    def batch_name(self):
        return self.batch.batch_name

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
        config=None,
        exclude=None,
        include=None,
    ):
        """Save the batch config"""
        if config is not None:
            self._config_ = config
        logger.info(f"Saving config to {self.batch.config_filepath}")
        cfg = XC.to_dict(self.config)
        if exclude is None:
            exclude = self.__config__.exclude

        if include:
            if isinstance(include, str):
                include = [include]
            args = {key: cfg[key] for key in include}
        else:
            args = cfg
            if exclude:
                if isinstance(exclude, str):
                    exclude = [exclude]
                for key in exclude:
                    args.pop(key, None)
        XC.save(args, self.batch.config_filepath)
        self.save_settings(exclude=exclude)
        return self.batch.config_filename

    def save_settings(self, exclude=None, exclude_none=True):
        def dumper(obj):
            return XC.to_dict(obj) if isinstance(obj, DictConfig) else str(obj)

        if exclude is None:
            exclude = self.__config__.exclude
        config = self.dict(exclude=exclude, exclude_none=exclude_none)
        if self.verbose:
            logger.info(f"Saving config to {self.batch.config_jsonpath}")
        XC.save_json(config, self.batch.config_jsonpath, default=dumper)

    def load_config(
        self,
        batch_name=None,
        batch_num=None,
        **args,
    ):
        """Load the config from the batch config file"""
        if self.verbose:
            logger.info(
                f"> Loading config for batch_name: {batch_name} batch_num: {batch_num}"
            )
        # self.config.batch.batch_num = batch_num
        if batch_name is None:
            batch_name = self.batch_name

        if batch_num is not None:
            cfg = self._initial_config_.copy()
            self.batch.batch_name = batch_name
            self.batch.batch_num = batch_num
            _path = self.batch.config_filepath
            if _path.is_file():
                logger.info(f"Loading config from {_path}")
                batch_cfg = XC.load(_path)
                if self.verbose:
                    logger.info("Merging config with the loaded config")
                cfg = XC.merge(cfg, batch_cfg)
            else:
                logger.info(f"No config file found at {_path}")
                batch_num = None
        else:
            cfg = self.config

        if self.verbose:
            logger.info(f"Merging config with args: {args}")
        self._config_ = XC.merge(cfg, args)

        self.batch_num = batch_num
        self.batch_name = batch_name

        return self.config

    def show_config(self, batch_name=None, batch_num=None):
        self.load_config(batch_name, batch_num)
        XC.print(self.dict())

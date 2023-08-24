"""
Configuration class for batch tasks. Inherits from TaskConfig.
"""
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from hyfi.batch import Batch
from hyfi.composer import Composer
from hyfi.path.batch import BatchPath
from hyfi.utils.logging import LOGGING

from .task import Task

logger = LOGGING.getLogger(__name__)


class BatchTask(Task):
    """
    Configuration class for batch tasks. Inherits from TaskConfig.

    Attributes:
        _config_name_ (str): The name of the configuration.
        _config_group_ (str): The configuration group.
        batch_name (str): The name of the batch.
        batch (BatchConfig): The batch configuration.
        _property_set_methods_ (Dict[str, str]): A dictionary of property set methods.
    """

    _config_name_: str = "__batch__"

    batch_name: str = "demo"
    batch: Batch = Batch()
    path: BatchPath = BatchPath()

    _property_set_methods_ = {
        "task_name": "set_task_name",
        "task_root": "set_task_root",
        "batch_name": "set_batch_name",
    }
    # _subconfigs_ = {"batch": BatchConfig}

    def set_batch_name(self, val: str):
        if not val:
            raise ValueError("Batch name cannot be empty")
        if not self.batch_name or self.batch_name != val:
            self.path.batch_name = val
            self.batch.batch_name = val

    def set_batch_num(self, val: Optional[int] = None):
        self.batch.batch_num = val

    def set_task_name(self, val: str):
        if not val:
            raise ValueError("Task name cannot be empty")
        if not self.task_name or self.task_name != val:
            self.path.task_name = val
            self.batch.batch_root = str(self.output_dir)

    def set_task_root(self, val: Union[str, Path]):
        if not val:
            raise ValueError("Task root cannot be empty")
        if not self.task_root or self.task_root != val:
            self.path.task_root = str(val)
            self.batch.batch_root = str(self.path.task_dir)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # At init, set the batch root to the task root
        # Othertimes, the batch root is set to the task root when the task root is set
        self.batch.batch_root = str(self.path.task_dir)
        # Call set_batch_num to set the batch_num and batch_id correctly after init
        if self.batch.batch_num_auto:
            self.batch.set_batch_num()
        logger.info(
            "Initalized batch: %s(%s) in %s",
            self.batch_name,
            self.batch_num,
            self.batch_dir,
        )

    @property
    def batch_num(self) -> int:
        return self.batch.batch_num

    @batch_num.setter
    def batch_num(self, val: Optional[int]):
        self.set_batch_num(val)

    @property
    def batch_id(self) -> str:
        return self.batch.batch_id

    @property
    def seed(self) -> int:
        return self.batch.seed

    @property
    def batch_dir(self) -> Path:
        return self.batch.batch_dir

    @property
    def device(self) -> str:
        return self.batch.device

    @property
    def num_devices(self) -> int:
        return self.batch.num_devices

    def save_config(
        self,
        filepath: Optional[Union[str, Path]] = None,
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
        save_as_json_as_well: bool = True,
    ) -> str:
        """
        Save the batch configuration to file.

        Args:
            filepath (Optional[Union[str, Path]]): The filepath to save the configuration to. Defaults to None.
            exclude (Optional[Union[str, List[str], Set[str], None]]): Keys to exclude from the saved configuration.
                Defaults to None.
            exclude_none (bool): Whether to exclude keys with None values from the saved configuration. Defaults to True.
            only_include (Optional[Union[str, List[str], Set[str], None]]): Keys to include in the saved configuration.
                Defaults to None.
            save_as_json_as_well (bool): Whether to save the configuration as a json file as well. Defaults to True.

        Returns:
            str: The filename of the saved configuration.
        """
        if not self.batch:
            raise ValueError("No batch configuration to save")
        if not filepath:
            filepath = self.batch.config_filepath

        if save_as_json_as_well:
            self.save_config_as_json(
                exclude=exclude,
                exclude_none=exclude_none,
                only_include=only_include,
            )
        return super().save_config(
            filepath=filepath,
            exclude=exclude,
            exclude_none=exclude_none,
            only_include=only_include,
        )

    def save_config_as_json(
        self,
        filepath: Optional[Union[str, Path]] = None,
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> str:
        if not self.batch:
            raise ValueError("No batch configuration to save")
        if not filepath:
            filepath = self.batch.config_jsonpath
        return super().save_config_as_json(
            filepath=filepath,
            exclude=exclude,
            exclude_none=exclude_none,
            only_include=only_include,
        )

    def load_config(
        self,
        batch_name: Optional[str] = None,
        batch_num: Optional[int] = None,
        filepath: Optional[Union[str, Path]] = None,
        **config_kwargs,
    ) -> Dict:
        """Load the config from the batch config file"""
        if not self.batch:
            raise ValueError("No batch configuration to load")
        if not batch_name:
            batch_name = self.batch_name
        if batch_num is None:
            batch_num = -1
        if not filepath and batch_num >= 0:
            batch = Batch(
                batch_root=self.batch.batch_root,
                batch_name=batch_name,
                batch_num=batch_num,
            )
            filepath = batch.config_filepath
        if isinstance(filepath, str):
            filepath = Path(filepath)

        if self.verbose:
            logger.info(
                "> Loading config for batch_name: %s batch_num: %s",
                batch_name,
                batch_num,
            )
        cfg = self.export_config()
        if filepath:
            if filepath.is_file():
                logger.info("Loading config from %s", filepath)
                batch_cfg = Composer.load(filepath)
                logger.info("Merging config with the loaded config")
                cfg = Composer.merge(cfg, batch_cfg)
            else:
                logger.info("No config file found at %s", filepath)
        if self.verbose:
            logger.info("Updating config with config_kwargs: %s", config_kwargs)
        cfg = Composer.update(Composer.to_dict(cfg), config_kwargs)

        # initialize self with the config
        self.__init__(**cfg)

        return self.model_dump()

    def print_config(
        self,
        batch_name: Optional[str] = None,
        batch_num: Optional[int] = None,
    ):
        self.load_config(batch_name, batch_num)
        Composer.print(self.model_dump())

"""This module contains the BatchConfig class, which is used to configure batch processing jobs.

The BatchConfig class inherits from the BaseConfig class and defines a set of configuration options
that can be used to customize batch processing jobs. These options include the batch name, batch number,
batch root directory, output suffix, output extension, random seed, device, number of devices, number of
workers, and configuration file names and directories.

The BatchConfig class also defines a set of methods for setting and validating configuration options,
including set_batch_num() and _validate_batch_num() for the batch number, and _validate_seed() for the
random seed.

Example usage:

    from hyfi.batch import BatchConfig

    config = BatchConfig(batch_name="my_batch", batch_num=1, batch_root="data", output_suffix="_out",
                         output_extension=".txt", random_seed=True, seed=42, resume_run=False,
                         resume_latest=False, device="cuda", num_devices=2, num_workers=4,
                         config_yaml="config.yaml", config_json="config.json", config_dirname="configs")
"""
import random
from pathlib import Path
from typing import Optional

from hyfi.composer import BaseConfig, FieldValidationInfo, field_validator
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BatchConfig(BaseConfig):
    """
    Configuration class for batch processing.

    Attributes:
        batch_name (str): Name of the batch.
        batch_num (Optional[int]): Number of the batch. If None, it will be set to -1.
        batch_root (str): Root directory for the batch.
        output_suffix (str): Suffix to be added to the output file name.
        output_extention (str): Extension of the output file.
        random_seed (bool): Whether to use a random seed for the batch.
        seed (int): Seed to be used for the batch. If random_seed is True or seed is None or negative, a random seed will be generated.
        resume_run (bool): Whether to resume a previous run of the batch.
        resume_latest (bool): Whether to resume the latest run of the batch.
        device (str): Device to be used for the batch.
        num_devices (int): Number of devices to be used for the batch.
        num_workers (int): Number of workers to be used for the batch.
        config_yaml (str): Name of the YAML configuration file.
        config_json (str): Name of the JSON configuration file.
        config_dirname (str): Name of the directory for the configuration files.
    """

    _config_name_: str = "__init__"
    _config_group_: str = "batch"

    batch_name: str
    batch_num: Optional[int] = None
    batch_root: str = "workspace/outputs"
    output_suffix: str = ""
    output_extention: str = ""
    random_seed: bool = True
    seed: int = -1
    resume_run: bool = False
    resume_latest: bool = False
    device: str = "cpu"
    num_devices: int = 1
    num_workers: int = 1
    config_yaml: str = "config.yaml"
    config_json: str = "config.json"
    config_dirname: str = "configs"

    _property_set_methods_ = {
        "batch_num": "set_batch_num",
    }

    def __init__(self, **data):
        """
        Initializes the BatchConfig object.

        Args:
            **data (dict): Dictionary containing the configuration data.
        """
        super().__init__(**data)
        self.set_batch_num(self.batch_num)

    def set_batch_num(self, val):
        """
        Sets the batch number.

        Args:
            val (int): Batch number.
        """
        if val is None:
            self.batch_num = -1
        if val < 0:
            num_files = len(list(self.config_dir.glob(self.config_filepattern)))
            self.batch_num = (
                num_files - 1 if self.resume_latest and num_files > 0 else num_files
            )
        if self.verbose:
            logger.info(
                "Init batch - Batch name: %s, Batch num: %s",
                self.batch_name,
                self.batch_num,
            )

    @field_validator("batch_num", mode="before")
    def _validate_batch_num(cls, v):
        """
        Validates the batch number.

        Args:
            v (int): Batch number.

        Returns:
            int: Validated batch number.
        """
        return v if v is not None else -1

    @field_validator("seed")
    def _validate_seed(cls, v, info: FieldValidationInfo):
        """
        Validates the seed.

        Args:
            v (int): Seed.
            info (FieldValidationInfo): Validation information.

        Returns:
            int: Validated seed.
        """
        if info.data["random_seed"] or v is None or v < 0:
            random.seed()
            seed = random.randint(0, 2**32 - 1)
            if info.data.get("verbose"):
                logger.info(f"Setting seed to {seed}")
            return seed
        return v

    @field_validator("output_suffix", mode="before")
    def _validate_output_suffix(cls, v):
        """
        Validates the output suffix.

        Args:
            v (str): Output suffix.

        Returns:
            str: Validated output suffix.
        """
        return v or ""

    @field_validator("output_extention", mode="before")
    def _validate_output_extention(cls, v):
        return v.strip(".") if v else ""

    @property
    def root_dir(self):
        """
        Root directory for the batch.
        """
        return Path(self.batch_root)

    @property
    def batch_dir(self):
        """
        Returns the path to the batch directory.
        """
        path_ = self.root_dir / self.batch_name
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def file_prefix(self):
        """
        Prefix for the output file name.
        """
        return f"{self.batch_name}({self.batch_num})"

    @property
    def output_file(self):
        """
        Output file name.
        """
        if self.output_suffix:
            return f"{self.file_prefix}_{self.output_suffix}.{self.output_extention}"
        else:
            return f"{self.file_prefix}.{self.output_extention}"

    @property
    def config_filename(self):
        """
        Name of the YAML configuration file.
        """
        return f"{self.file_prefix}_{self.config_yaml}"

    @property
    def config_jsonfile(self):
        """
        Name of the JSON configuration file.
        """
        return f"{self.file_prefix}_{self.config_json}"

    @property
    def config_filepattern(self):
        """
        File pattern for the configuration files.
        """
        return f"{self.batch_name}(*)_{self.config_yaml}"

    @property
    def config_dir(self):
        """
        Directory for the configuration files.
        """
        config_dir = self.batch_dir / self.config_dirname
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    @property
    def config_filepath(self):
        """
        Path to the YAML configuration file.
        """
        return self.config_dir / self.config_filename

    @property
    def config_jsonpath(self):
        """
        Path to the JSON configuration file.
        """
        return self.config_dir / self.config_jsonfile

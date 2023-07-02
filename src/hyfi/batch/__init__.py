import random
from pathlib import Path
from typing import Optional

from pydantic import FieldValidationInfo, field_validator

from hyfi.composer import BaseConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BatchConfig(BaseConfig):
    _config_name_: str = "__init__"
    _config_group_: str = "batch"

    batch_name: str
    batch_num: Optional[int] = None
    batch_root: str = "outputs"
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
        super().__init__(**data)
        self.set_batch_num(self.batch_num)

    def set_batch_num(self, val):
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
        return v if v is not None else -1

    @field_validator("seed")
    def _validate_seed(cls, v, info: FieldValidationInfo):
        if info.data["random_seed"] or v is None or v < 0:
            random.seed()
            seed = random.randint(0, 2**32 - 1)
            if info.data.get("verbose"):
                logger.info(f"Setting seed to {seed}")
            return seed
        return v

    @field_validator("output_suffix", mode="before")
    def _validate_output_suffix(cls, v):
        return v or ""

    @field_validator("output_extention", mode="before")
    def _validate_output_extention(cls, v):
        return v.strip(".") if v else ""

    @property
    def root_dir(self):
        return Path(self.batch_root)

    @property
    def batch_dir(self):
        self.root_dir.mkdir(parents=True, exist_ok=True)
        return self.root_dir

    @property
    def config_dir(self):
        config_dir = self.batch_dir / self.config_dirname
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    @property
    def file_prefix(self):
        return f"{self.batch_name}({self.batch_num})"

    @property
    def output_file(self):
        if self.output_suffix:
            return f"{self.file_prefix}_{self.output_suffix}.{self.output_extention}"
        else:
            return f"{self.file_prefix}.{self.output_extention}"

    @property
    def config_filename(self):
        return f"{self.file_prefix}_{self.config_yaml}"

    @property
    def config_jsonfile(self):
        return f"{self.file_prefix}_{self.config_json}"

    @property
    def config_filepattern(self):
        return f"{self.batch_name}(*)_{self.config_yaml}"

    @property
    def config_filepath(self):
        return self.config_dir / self.config_filename

    @property
    def config_jsonpath(self):
        return self.config_dir / self.config_jsonfile

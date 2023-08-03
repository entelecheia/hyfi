from pathlib import Path

from hyfi.utils.logging import LOGGING

from .task import TaskPathConfig

logger = LOGGING.getLogger(__name__)


class BatchPathConfig(TaskPathConfig):
    _config_name_: str = "__batch__"

    batch_name: str = "demo-batch"

    @property
    def batch_dir(self) -> Path:
        """
        Returns the path to the batch directory.
        """
        path_ = self.output_dir / self.batch_name
        path_.mkdir(parents=True, exist_ok=True)
        return path_

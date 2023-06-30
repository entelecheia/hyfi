import os
from hyfi.task.batch import BatchTaskConfig
from pathlib import Path
from pprint import pprint


def test_batch_task_config():
    os.environ["HYFI_LOG_LEVEL"] = "DEBUG"
    config = BatchTaskConfig(
        task_name="demo2",
        batch_name="batch11",
    )
    pprint(config.batch.dict())
    # Test that the default values are set correctly

    assert config.batch.batch_name == "batch11"
    # Test that the log_dir and cache_dir properties return the correct values
    assert Path(config.log_dir).is_dir()
    assert Path(config.cache_dir).is_dir()
    config.save_config()
    cfg = config.load_config(batch_num=1)
    pprint(cfg)


if __name__ == "__main__":
    test_batch_task_config()

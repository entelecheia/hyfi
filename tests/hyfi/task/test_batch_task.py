import os
from hyfi.task.batch import BatchTask
from pathlib import Path
from pprint import pprint


def test_batch_task_config():
    os.environ["HYFI_LOG_LEVEL"] = "DEBUG"
    config = BatchTask(
        task_name="demo2",
        batch_name="batch11",
        verbose=True,
    )
    pprint(config.batch.model_dump())
    # Test that the default values are set correctly

    assert config.batch.batch_name == "batch11"
    # Test that the log_dir and cache_dir properties return the correct values
    config.save_config()
    config.batch_num = 2222
    config.save_config()
    cfg = config.load_config(batch_num=2222)
    # config.print_config()
    # pprint(config.batch.model_dump())
    assert cfg["batch"]["batch_num"] == 2222


if __name__ == "__main__":
    test_batch_task_config()

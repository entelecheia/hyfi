from hyfi.task import TaskConfig
from pathlib import Path
from pprint import pprint


def test_task_config():
    config = TaskConfig(
        task_name="demo2",
    )
    pprint(config.dict())
    # Test that the default values are set correctly

    assert config.project.task_name == "demo2"
    # Test that the log_dir and cache_dir properties return the correct values
    assert Path(config.log_dir).is_dir()
    assert Path(config.cache_dir).is_dir()


if __name__ == "__main__":
    test_task_config()

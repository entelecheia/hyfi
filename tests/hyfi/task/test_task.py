from hyfi.task import TaskConfig
from pathlib import Path
from pprint import pprint


def test_task_config():
    config = TaskConfig(
        task_name="demo2",
        verbose=True,
    )
    pprint(config.model_dump())
    # Test that the default values are set correctly

    assert config.task_name == "demo2"
    # Test that the log_dir and cache_dir properties return the correct values
    assert Path(config.log_dir).is_dir()
    assert Path(config.cache_dir).is_dir()

    config.task_name = "demo3"
    pprint(config.model_dump())
    # Test that the default values are set correctly
    print(config.task_dir)
    assert config.task_dir == Path("workspace/tasks/demo3")
    config.task_root = "workspace/tmp"
    config.print_config()
    print(config.root_dir)
    assert config.task_dir == Path("workspace/tmp/demo3")


if __name__ == "__main__":
    test_task_config()

from hyfi.task import Task
from pathlib import Path
from pprint import pprint
from hyfi.main import HyFI


def test_task_config():
    HyFI.initialize(project_root=".")
    config = Task(
        task_name="demo2",
        verbose=True,
    )
    pprint(config.model_dump())
    # Test that the default values are set correctly

    assert config.task_name == "demo2"
    # Test that the log_dir and cache_dir properties return the correct values

    config.task_name = "demo3"
    pprint(config.model_dump())
    # Test that the default values are set correctly
    print(config.task_dir)
    assert config.task_dir == Path("workspace/demo3").absolute()
    config.task_root = "workspace/tmp"
    config.print_config()
    print(config.root_dir)
    assert config.task_dir == Path("workspace/tmp/demo3").absolute()
    config.save_config(filepath=config.path.config_filepath)


if __name__ == "__main__":
    test_task_config()

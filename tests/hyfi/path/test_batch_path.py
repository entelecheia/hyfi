from hyfi.path.batch import BatchPath
from pathlib import Path
from pprint import pprint
from hyfi import HyFI


def test_path_config():
    HyFI.initialize(project_root=".")
    config = BatchPath(
        task_root="workspace/tasks",
        task_name="test-task",
    )
    pprint(config.model_dump())
    # Test that the default values are set correctly
    assert config._config_name_ == "__batch__"
    config.batch_name = "test-batch"
    print(config.batch_dir)
    assert config.batch_dir == Path("workspace/tasks/test-task/test-batch").absolute()


if __name__ == "__main__":
    test_path_config()

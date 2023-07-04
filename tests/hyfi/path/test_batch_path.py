from hyfi.path.batch import BatchPathConfig
from pathlib import Path
from pprint import pprint


def test_path_config():
    config = BatchPathConfig(
        task_root="workspace/tasks",
        task_name="test-task",
    )
    pprint(config.model_dump())
    # Test that the default values are set correctly
    assert config._config_name_ == "__batch__"
    config.batch_name = "test-batch"
    print(config.batch_dir)
    assert (
        config.batch_dir
        == Path("workspace/tasks/test-task/outputs/test-batch")
    )

    # Test that the log_dir is created
    assert Path(config.log_dir).is_dir()


if __name__ == "__main__":
    test_path_config()

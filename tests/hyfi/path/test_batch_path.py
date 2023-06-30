from hyfi.path.batch import BatchPathConfig
from pathlib import Path
from pprint import pprint


def test_path_config():
    config = BatchPathConfig(task_root="workspace/test_task")
    pprint(config.dict())
    # Test that the default values are set correctly
    assert config._config_name_ == "__batch__"
    print(config.batch_dir)
    assert (
        config.batch_dir == Path("workspace/test_task/outputs/batch-outputs").absolute()
    )

    # Test that the log_dir is created
    assert Path(config.log_dir).is_dir()


if __name__ == "__main__":
    test_path_config()

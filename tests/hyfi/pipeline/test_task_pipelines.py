from hyfi.main import HyFI
from hyfi.task import TaskConfig


def test_task_config():
    config = TaskConfig(config_name="__test__")
    HyFI.print(config.dict())
    HyFI.run_task_pipelines(config)


if __name__ == "__main__":
    test_task_config()

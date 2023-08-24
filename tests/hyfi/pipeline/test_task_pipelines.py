from hyfi.main import HyFI
from hyfi.task import TaskConfig
from hyfi.project import Project


def test_task_config():
    HyFI.initialize(
        project_name="run_task", project_root="workspace/run_task", num_workers=2
    )

    task = TaskConfig(_config_name_="__test__")
    HyFI.print(task.model_dump())
    HyFI.run_task(task)
    HyFI.print(task.model_dump())


if __name__ == "__main__":
    test_task_config()

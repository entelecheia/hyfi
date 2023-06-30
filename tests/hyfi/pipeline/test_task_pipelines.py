from hyfi.main import HyFI
from hyfi.task import TaskConfig
from hyfi.project import ProjectConfig


def test_task_config():
    project = ProjectConfig(
        project_name="run_task", project_root="workspace/run_task", num_workers=2
    )

    task = TaskConfig(_config_name_="__test__")
    HyFI.print(task.dict())
    HyFI.run_task(task, project=project)
    HyFI.print(task.dict())


if __name__ == "__main__":
    test_task_config()

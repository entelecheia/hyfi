import os
from hyfi.main import HyFI
from hyfi._version import __version__
from pprint import pprint


def test_version():
    assert HyFI.__version__ == __version__


def test_envs():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    envs = HyFI.dotenv()
    pprint(envs.dict())
    assert envs.HYFI_PROJECT_NAME == "hyfi"


def test_init_workspace():
    os.environ["HYFI_PROJECT_ROOT"] = ""
    ws = HyFI.init_workspace(
        project_name="hyfi2",
        global_hyfi_root="tmp",
        global_workspace_name="testspace",
        task_name="test",
        log_level="WARNING",
        verbose=True,
    )
    pprint(ws.dict())
    assert ws.path.project_root == "tmp/testspace/projects/hyfi2"


def test_compose():
    os.environ["HYFI_PROJECT_ROOT"] = "."
    cfg = HyFI.compose("path=__task__")
    print(cfg["task_root"])
    assert cfg["task_root"] == "./tmp"


if __name__ == "__main__":
    test_version()
    test_envs()
    test_init_workspace()
    test_compose()

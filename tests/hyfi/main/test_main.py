import os
from hyfi.main import HyFI
from hyfi._version import __version__
from pprint import pprint


def test_about():
    print(HyFI.print_about())


def test_version():
    assert HyFI.__version__ == __version__


def test_envs():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    env = HyFI.Env()
    pprint(env.model_dump())
    assert env.HYFI_PROJECT_NAME == "hyfi"


def test_init_project():
    os.environ["HYFI_PROJECT_ROOT"] = ""
    h = HyFI.initialize(
        project_name="hyfi2",
        global_hyfi_root="workspace",
        global_workspace_name="testspace",
        log_level="WARNING",
        verbose=True,
    )
    prj = h.project
    pprint(prj.model_dump())
    assert prj.path.global_workspace_name == "testspace"
    print(h.variables)


def test_compose():
    os.environ["HYFI_PROJECT_ROOT"] = "."
    cfg = HyFI.compose("path=__task__")
    print(cfg["task_root"])
    assert cfg["task_root"] == "workspace"


if __name__ == "__main__":
    test_about()
    test_version()
    test_envs()
    test_init_project()
    test_compose()

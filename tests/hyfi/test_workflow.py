"""
test workflow
"""
import subprocess
from typing import List, Tuple
from hyfi.main import HyFI


def capture(command: List[str]) -> Tuple[bytes, bytes, int]:
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_cli_run_workflow() -> None:
    """Test cli command run_workflow"""
    command = [
        "poetry",
        "run",
        "hyfi",
        "cmd=run_workflow",
        "workflow=__test__",
    ]
    out, err, exitcode = capture(command)
    assert exitcode == 0


def test_worflow() -> None:
    """Test workflow"""
    wf = HyFI.workflow(_config_name_="__test__")
    HyFI.print(wf.model_dump())
    HyFI.run_workflow(wf)


if __name__ == "__main__":
    test_worflow()

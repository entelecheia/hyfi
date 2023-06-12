"""
test cli module
"""
import subprocess
from typing import List, Tuple
from hyfi.__cli__ import hydra_main


def capture(command: List[str]) -> Tuple[bytes, bytes, int]:
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_cli() -> None:
    """Test cli module"""
    command = ["poetry", "run", "hyfi"]
    out, err, exitcode = capture(command)
    assert exitcode == 0


def manual_test_hydra_main() -> None:
    """Test hydra_main function"""
    hydra_main()


if __name__ == "__main__":
    manual_test_hydra_main()

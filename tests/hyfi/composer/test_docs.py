from hyfi.composer import DocGenerator
from typing import List, Tuple
import subprocess


def capture(command: List[str]) -> Tuple[bytes, bytes, int]:
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_generate_configs():
    DocGenerator.generate_config()
    DocGenerator.generate_config()


def generate_docs():
    dg = DocGenerator()
    dg.generate_config_docs()
    dg.generate_reference_docs()


def test_generate_docs() -> None:
    command = ["poetry", "run", "hyfi", "+docs=__init__"]
    out, err, exitcode = capture(command)
    assert exitcode == 0


if __name__ == "__main__":
    test_generate_configs()
    generate_docs()

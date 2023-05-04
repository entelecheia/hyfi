import os
import shutil
from pathlib import Path

import pytest

from hyfi.utils.copier import Copier


def test_files_are_copied(tmp_path):
    # source path is under src/hyfi/conf
    src_path = Path("src/hyfi/conf")
    assert src_path.exists()
    dst_path = tmp_path / "output"

    with Copier(src_path=src_path, dst_path=dst_path, verbose=False) as worker:
        worker.run_copy()

    for root, _, files in os.walk(src_path):
        for filename in files:
            if filename.endswith(".yaml"):
                src_file = Path(root, filename)
                dst_file = dst_path / src_file.relative_to(src_path)
                assert dst_file.exists()


def test_cleanup_on_error(tmp_path):
    src_path = Path("src/hyfi/conf")
    assert src_path.exists()
    dst_path = tmp_path / "output"

    with pytest.raises(Exception):
        with Copier(src_path=src_path, dst_path=dst_path, verbose=False) as worker:
            worker.run_copy()
            raise Exception("Simulated error")

    assert not dst_path.exists()


def test_no_cleanup_on_error_if_dst_existed(tmp_path):
    src_path = Path("src/hyfi/conf")
    assert src_path.exists()
    dst_path = tmp_path / "output"
    dst_path.mkdir(parents=True, exist_ok=True)

    with pytest.raises(Exception):
        with Copier(src_path=src_path, dst_path=dst_path, verbose=False) as worker:
            worker.run_copy()
            raise Exception("Simulated error")

    assert dst_path.exists()
    shutil.rmtree(dst_path)


if __name__ == "__main__":
    pytest.main(["-v", "test_copier.py"])

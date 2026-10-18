import os
import sys
import textwrap
from pathlib import Path

import pytest

PLUGIN_FILES = {
    "fakeplug/__init__.py": "",
    "fakeplug/steps.py": """
        def load(n=3):
            return list(range(n))

        def double(xs):
            return [x * 2 for x in xs]

        def total(xs):
            return sum(xs)

        def constant(value=7):
            return value

        def boom(*args, **kwargs):
            raise ValueError("boom")

        def fail_with(msg):
            raise ValueError(f"failed with {msg}")
    """,
    "fakeplug/conf/__init__.py": "",
    "fakeplug/conf/workflow/plug.yaml": """
        name: plug
        steps:
          - run: fakeplug.steps.load
            with: {n: 4}
          - run: fakeplug.steps.double
          - run: fakeplug.steps.total
    """,
    "fakeplug/conf/tokenizer/simple.yaml": """
        lowercase: true
        min_len: 2
    """,
    "fakeplug-0.1.dist-info/METADATA": """
        Metadata-Version: 2.1
        Name: fakeplug
        Version: 0.1
    """,
    "fakeplug-0.1.dist-info/entry_points.txt": """
        [hyfi.plugins]
        fakeplug = fakeplug.conf
        ghost = ghost_missing.conf
    """,
}


def write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")


@pytest.fixture
def project(tmp_path, monkeypatch):
    """An isolated cwd with no HYFI_* env and the fake plugin installed on sys.path."""
    for key in list(sys.modules):
        if key == "fakeplug" or key.startswith("fakeplug."):
            del sys.modules[key]
    site = tmp_path / "site"
    write_tree(site, PLUGIN_FILES)
    monkeypatch.syspath_prepend(str(site))
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    for key in [k for k in list(os.environ) if k.startswith("HYFI_")]:
        monkeypatch.delenv(key)
    return work

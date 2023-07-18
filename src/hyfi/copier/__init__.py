"""
This module contains the Copier class, which represents the state of a copier
work and contains methods to actually produce the desired work.

To use it properly, use it as a context manager and fill all dataclass fields.

    try:
        with Copier(
            src_path=Path("source"),
            dst_path=Path("output"),
            exclude=["*.bak"],
            skip_if_exists=[".gitignore"],
            cleanup_on_error=True,
            overwrite=False,
            dry_run=False,
            verbose=True,
        ) as worker:
            worker.run_copy()
    except Exception as e:
        print(f"Error: {e}")

"""

import filecmp
import os
from dataclasses import field
from pathlib import Path
from shutil import copy2, rmtree
from typing import List, Optional, Union

from pathspec import PathSpec
from pydantic.dataclasses import dataclass

from hyfi.utils.envs import ENVs
from hyfi.utils.funcs import FUNCs, Style


@dataclass()
class Copier:
    """Copier process state manager.

    This class represents the state of a copier work and contains methods to
    actually produce the desired work.

    To use it properly, use it as a context manager and fill all dataclass fields.

    Then, execute `run_copy` to copy the template to the destination.

    Attributes:
        src_path:
            Source path where to find the template.

        dst_path:
            Destination path where to render the template.

        filetypes:
            Filetypes to copy.

        exclude:
            User-chosen additional file exclusion patterns.

        exclude_test_files:
            If `True`, exclude files that match the patterns for testing. (default: True)

        skip_if_exists:
            If `True`, skip files that already exist in the destination. (default: False)

        cleanup_on_error:
            Delete `dst_path` if there's an error?

        overwrite:
            When `True`, Overwrite files that already exist, without asking.

        dry_run:
            When `True`, produce no real rendering.

        verbose:
            When `True`, show all output.
    """

    src_path: Path = field(default=Path("conf"))
    dst_path: Path = field(default=Path("."))
    filetypes: Optional[Union[List[str], str]] = field(default=None)
    exclude: Optional[Union[List[str], str]] = field(default=None)
    exclude_test_files: bool = True
    skip_if_exists: bool = False
    cleanup_on_error: bool = True
    overwrite: bool = False
    dry_run: bool = False
    verbose: bool = True

    def __post_init__(self):
        """Initialize the path_spec attribute based on the exclude patterns."""
        # Validate and convert src_path and dst_path
        for attr_name in ["src_path", "dst_path"]:
            attr_value = getattr(self, attr_name)
            if not isinstance(attr_value, Path):
                setattr(self, attr_name, Path(attr_value))

        # Validate and convert exclude and filetypes
        for attr_name in ["exclude", "filetypes"]:
            attr_value = getattr(self, attr_name)
            if attr_value is None:
                setattr(self, attr_name, [])
            elif not isinstance(attr_value, list):
                setattr(self, attr_name, [attr_value])

        if self.filetypes is None or len(self.filetypes) == 0:
            self.filetypes = ["yaml", "yml", "py"]

        exclude = (
            []
            if self.exclude is None or len(self.exclude) == 0
            else [self.exclude]
            if isinstance(self.exclude, str)
            else self.exclude
        )

        test_files = ["_test_*", "__test_*"]
        if self.exclude_test_files:
            exclude += test_files
        if not self.dst_path.is_absolute():
            self.dst_path = ENVs.getcwd() / self.dst_path
        self.path_spec = PathSpec.from_lines("gitwildmatch", exclude)
        self.dst_path_existed = self.dst_path.exists()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager, handling cleanup if needed."""
        if exc_type is not None and not self.dst_path_existed and self.cleanup_on_error:
            rmtree(self.dst_path)
            FUNCs.printf(
                "CLEANUP",
                f"Removed {self.dst_path}",
                Style.DANGER,
                verbose=self.verbose,
            )

    def run_copy(self):
        """Execute the copy process.

        Walk through the source directory, compare YAML files with the destination
        directory, and copy files based on the specified settings.
        """
        if not Path(self.src_path).is_dir():
            FUNCs.printf(
                "ERROR",
                f"Source path {self.src_path} does not exist.",
                style=Style.DANGER,
            )
            return
        for root, _, files in os.walk(self.src_path):
            for filename in files:
                if not any(filename.endswith(filetype) for filetype in self.filetypes):
                    continue

                src_file = Path(root, filename)
                dst_file = self.dst_path / src_file.relative_to(self.src_path)
                dst_file = dst_file.absolute()

                if self.path_spec.match_file(src_file):
                    FUNCs.printf(
                        "EXCLUDED", f"{src_file}", Style.WARNING, verbose=self.verbose
                    )
                    continue

                if dst_file.exists():
                    if self.skip_if_exists:
                        FUNCs.printf(
                            "SKIPPED",
                            f"{src_file}",
                            Style.WARNING,
                            verbose=self.verbose,
                        )
                        continue

                    if filecmp.cmp(src_file, dst_file, shallow=False):
                        FUNCs.printf(
                            "UNCHANGED",
                            f"{src_file}",
                            Style.IGNORE,
                            verbose=self.verbose,
                        )
                        continue

                    answer = "Y"
                    if not self.overwrite:
                        answer = input(f"Overwrite {dst_file}? [Y/n]: ") or "Y"
                    if answer.lower() != "y":
                        FUNCs.printf(
                            "IGNORED",
                            f"{src_file}",
                            Style.WARNING,
                            verbose=self.verbose,
                        )
                        continue

                if not self.dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    copy2(src_file, dst_file)
                FUNCs.printf(
                    "COPIED",
                    f"{src_file} -> {dst_file}",
                    Style.OK,
                    verbose=self.verbose,
                )

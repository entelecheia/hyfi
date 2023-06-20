"""File I/O functions"""
import errno
import os
import re
import shutil
import stat
import sys
import tempfile
import time
import warnings
from glob import glob
from pathlib import Path, PosixPath, WindowsPath
from types import TracebackType
from typing import Callable, List, Tuple, Union

from hyfi.utils.logging import getLogger

logger = getLogger(__name__)

PathLikeType = Union[str, PosixPath, WindowsPath]


class IOLibs:
    @staticmethod
    def is_valid_regex(expr: str) -> bool:
        """Check if a string is a valid regular expression"""
        try:
            if expr.startswith("r:"):
                expr = expr[2:]
            else:
                return False
            re.compile(expr)
            return True
        except re.error:
            return False

    @staticmethod
    def glob_re(
        pattern: str,
        base_dir: str,
        recursive: bool = False,
    ) -> list:
        """Glob files matching a regular expression"""
        if IOLibs.is_valid_regex(pattern):
            pattern = pattern[2:]
            rpattern = re.compile(pattern)  # type: ignore
            files = []
            if recursive:
                for dirpath, dirnames, filenames in os.walk(base_dir):
                    files += [
                        os.path.join(dirpath, file)
                        for file in filenames
                        if rpattern.search(file)
                    ]
            else:
                files = [
                    os.path.join(base_dir, file)
                    for file in os.listdir(base_dir)
                    if rpattern.search(file)
                ]
        else:
            file = os.path.join(base_dir, pattern) if base_dir else pattern
            files = glob(file, recursive=recursive)
        return files

    @staticmethod
    def get_filepaths(
        filename_patterns: Union[List[PathLikeType], PathLikeType],
        base_dir: Union[str, PosixPath, WindowsPath] = "",
        recursive: bool = True,
        verbose: bool = False,
        **kwargs,
    ) -> List[str]:
        """Get a list of filepaths from a list of filename patterns"""
        if filename_patterns is None:
            raise ValueError("filename_patterns must be specified")
        if isinstance(filename_patterns, (PosixPath, WindowsPath)):
            filename_patterns = str(filename_patterns)
        if isinstance(filename_patterns, str):
            filename_patterns = [filename_patterns]
        filepaths = []
        base_dir = str(base_dir) if base_dir else ""
        for file in filename_patterns:
            file = str(file)
            filepath = os.path.join(base_dir, file) if base_dir else file
            if os.path.exists(filepath):
                if Path(filepath).is_file():
                    filepaths.append(filepath)
            else:
                if os.path.dirname(file) != "":
                    _dir = os.path.dirname(file)
                    file = os.path.basename(file)
                    base_dir = os.path.join(base_dir, _dir) if base_dir else _dir
                filepaths += IOLibs.glob_re(file, base_dir, recursive=recursive)
        filepaths = [fp for fp in filepaths if Path(fp).is_file()]
        if verbose:
            logger.info(f"Processing [{len(filepaths)}] files from {filename_patterns}")

        return filepaths

    @staticmethod
    def get_files_from_archive(archive_path: str, filetype: str = ""):
        """Get a list of files from an archive"""
        import tarfile
        from zipfile import ZipFile

        if ".tar.gz" in archive_path:
            logger.info(f"::Extracting files from {archive_path} with tar.gz")
            archive_handle = tarfile.open(archive_path, "r:gz")
            files = [
                (file, file.name)
                for file in archive_handle.getmembers()
                if file.isfile()
            ]
            open_func = archive_handle.extractfile
        elif ".tar.bz2" in archive_path:
            logger.info(f"::Extracting files from {archive_path} with tar.bz2")
            archive_handle = tarfile.open(archive_path, "r:bz2")
            files = [
                (file, file.name)
                for file in archive_handle.getmembers()
                if file.isfile()
            ]
            open_func = archive_handle.extractfile
        elif ".zip" in archive_path:
            logger.info(f"::Extracting files from {archive_path} with zip")
            archive_handle = ZipFile(archive_path)
            files = [
                (file, file.encode("cp437").decode("euc-kr"))
                for file in archive_handle.namelist()
            ]
            open_func = archive_handle.open
        else:
            # print(f'::{archive_path} is not archive, use generic method')
            files = [(archive_path, os.path.basename(archive_path))]
            archive_handle = None
            open_func = None
        if filetype:
            files = [file for file in files if filetype in file[1]]

        return files, archive_handle, open_func

    @staticmethod
    def read(uri, mode="rb", encoding=None, head=None, **kwargs) -> bytes:
        """Read data from a file or url"""
        uri = str(uri)
        if uri.startswith("http"):
            import requests

            if mode == "r" and head is not None and isinstance(head, int):
                r = requests.get(uri, stream=True)
                r.raw.decode_content = True
                return r.raw.read(head)
            return requests.get(uri, **kwargs).content
        # elif uri.startswith("s3://"):
        #     import boto3

        #     s3 = boto3.resource("s3")
        #     bucket, key = uri.replace("s3://", "").split("/", 1)
        #     obj = s3.Object(bucket, key)
        #     return obj.get()["Body"].read()
        else:
            with open(uri, mode=mode, encoding=encoding) as f:
                if mode == "r" and head is not None and isinstance(head, int):
                    return f.read(head)
                return f.read()

    @staticmethod
    def is_file(a, *p) -> bool:
        """Check if path is a file"""
        _path = os.path.join(a, *p)
        return Path(_path).is_file()

    @staticmethod
    def is_dir(a, *p) -> bool:
        """Check if path is a directory"""
        _path = os.path.join(a, *p)
        return Path(_path).is_dir()

    def check_path(_path: str, alt_path: str = "") -> str:
        """Check if path exists, return alt_path if not"""
        return _path if os.path.exists(_path) else alt_path

    @staticmethod
    def mkdir(_path: str) -> str:
        """Create directory if it does not exist"""
        if _path is None:
            return ""
        Path(_path).mkdir(parents=True, exist_ok=True)
        return _path

    @staticmethod
    def exists(a, *p) -> bool:
        """Check if path exists"""
        if a is None:
            return False
        _path = os.path.join(a, *p)
        return os.path.exists(_path)

    @staticmethod
    def join_path(a, *p) -> str:
        """Join path components intelligently."""
        if not p or p[0] is None:
            return a
        p = [str(_p) for _p in p]
        return os.path.join(*p) if a is None else os.path.join(a, *p)

    @staticmethod
    def copy(src, dst, *, follow_symlinks=True):
        """
        Copy a file or directory. This is a wrapper around shutil.copy.
        If you need to copy an entire directory (including all of its contents), or if you need to overwrite existing files in the destination directory, shutil.copy() would be a better choice.

        Args:
                src: Path to the file or directory to be copied.
                dst: Path to the destination directory. If the destination directory does not exist it will be created.
                follow_symlinks: Whether or not symlinks should be followed
        """
        import shutil

        src = str(src)
        dst = str(dst)
        IOLibs.mkdir(dst)
        shutil.copy(src, dst, follow_symlinks=follow_symlinks)
        logger.info(f"copied {src} to {dst}")

    @staticmethod
    def copyfile(src, dst, *, follow_symlinks=True):
        """
        Copy a file or directory. This is a wrapper around shutil.copyfile.
        If you want to copy a single file from one location to another, shutil.copyfile() is the appropriate function to use.

        Args:
                src: Path to the file or directory to copy.
                dst: Path to the destination file or directory. If the destination file already exists it will be overwritten.
                follow_symlinks: Whether to follow symbolic links or not
        """
        import shutil

        src = str(src)
        dst = str(dst)
        shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)
        logger.info(f"copied {src} to {dst}")

    @staticmethod
    def get_modified_time(path):
        """Return the modification time of a file"""
        if not os.path.exists(path):
            return None
        modTimesinceEpoc = os.path.getmtime(path)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modTimesinceEpoc))

    @staticmethod
    def handle_remove_readonly(
        func: Callable, path: str, exc: Tuple[BaseException, OSError, TracebackType]
    ) -> None:
        """Handle errors when trying to remove read-only files through `shutil.rmtree`.

        This handler makes sure the given file is writable, then re-execute the given removal function.

        Arguments:
            func: An OS-dependant function used to remove a file.
            path: The path to the file to remove.
            exc: A `sys.exc_info()` object.
        """
        excvalue = exc[1]
        if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(path)
        else:
            raise

    @staticmethod
    def copy_file(src_path: Path, dst_path: Path, follow_symlinks: bool = True) -> None:
        """Copy one file to another place."""
        shutil.copy2(src_path, dst_path, follow_symlinks=follow_symlinks)

    @staticmethod
    def readlink(link: Path) -> Path:
        """A custom version of os.readlink/pathlib.Path.readlink.

        pathlib.Path.readlink is what we ideally would want to use, but it is only available on python>=3.9.
        os.readlink doesn't support Path and bytes on Windows for python<3.8
        """
        if sys.version_info >= (3, 9):
            return link.readlink()
        elif sys.version_info >= (3, 8) or os.name != "nt":
            return Path(os.readlink(link))
        else:
            return Path(os.readlink(str(link)))


# See https://github.com/copier-org/copier/issues/345
class TemporaryDirectory(tempfile.TemporaryDirectory):
    """A custom version of `tempfile.TemporaryDirectory` that handles read-only files better.

    On Windows, before Python 3.8, `shutil.rmtree` does not handle read-only files very well.
    This custom class makes use of a [special error handler][copier.tools.handle_remove_readonly]
    to make sure that a temporary directory containing read-only files (typically created
    when git-cloning a repository) is properly cleaned-up (i.e. removed) after using it
    in a context manager.
    """

    @classmethod
    def _cleanup(cls, name, warn_message):
        cls._robust_cleanup(name)
        warnings.warn(warn_message, ResourceWarning)

    def cleanup(self):
        """Remove directory safely."""
        if self._finalizer.detach():  # type: ignore
            self._robust_cleanup(self.name)

    @staticmethod
    def _robust_cleanup(name):
        shutil.rmtree(name, ignore_errors=False, onerror=IOLibs.handle_remove_readonly)

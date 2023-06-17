"""File I/O functions"""
import os
import re
from glob import glob
from pathlib import Path, PosixPath, WindowsPath
from typing import List, Union

from hyfi.utils.logging import getLogger

logger = getLogger(__name__)

PathLikeType = Union[str, PosixPath, WindowsPath]


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


def glob_re(
    pattern: str,
    base_dir: str,
    recursive: bool = False,
) -> list:
    """Glob files matching a regular expression"""
    if is_valid_regex(pattern):
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
            filepaths += glob_re(file, base_dir, recursive=recursive)
    filepaths = [fp for fp in filepaths if Path(fp).is_file()]
    if verbose:
        logger.info(f"Processing [{len(filepaths)}] files from {filename_patterns}")

    return filepaths


def get_files_from_archive(archive_path: str, filetype: str = ""):
    """Get a list of files from an archive"""
    import tarfile
    from zipfile import ZipFile

    if ".tar.gz" in archive_path:
        logger.info(f"::Extracting files from {archive_path} with tar.gz")
        archive_handle = tarfile.open(archive_path, "r:gz")
        files = [
            (file, file.name) for file in archive_handle.getmembers() if file.isfile()
        ]
        open_func = archive_handle.extractfile
    elif ".tar.bz2" in archive_path:
        logger.info(f"::Extracting files from {archive_path} with tar.bz2")
        archive_handle = tarfile.open(archive_path, "r:bz2")
        files = [
            (file, file.name) for file in archive_handle.getmembers() if file.isfile()
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


def is_file(a, *p) -> bool:
    """Check if path is a file"""
    _path = os.path.join(a, *p)
    return Path(_path).is_file()


def is_dir(a, *p) -> bool:
    """Check if path is a directory"""
    _path = os.path.join(a, *p)
    return Path(_path).is_dir()


def check_path(_path: str, alt_path: str = "") -> str:
    """Check if path exists, return alt_path if not"""
    return _path if os.path.exists(_path) else alt_path


def mkdir(_path: str) -> str:
    """Create directory if it does not exist"""
    if _path is None:
        return ""
    Path(_path).mkdir(parents=True, exist_ok=True)
    return _path


def exists(a, *p) -> bool:
    """Check if path exists"""
    if a is None:
        return False
    _path = os.path.join(a, *p)
    return os.path.exists(_path)


def join_path(a, *p) -> str:
    """Join path components intelligently."""
    if not p or p[0] is None:
        return a
    p = [str(_p) for _p in p]
    return os.path.join(*p) if a is None else os.path.join(a, *p)

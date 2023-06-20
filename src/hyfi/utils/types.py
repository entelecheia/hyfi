from enum import Enum
from os import PathLike
from pathlib import PosixPath, WindowsPath
from typing import Any, List, Sequence, Union

from omegaconf import ListConfig

IntSeq = Sequence[int]
ListLike = Union[ListConfig, List, Sequence[Any]]
DictKeyType = Union[str, bytes, int, Enum, float, bool]
PathOrStr = Union[str, PathLike]
PathLikeType = Union[str, PosixPath, WindowsPath]

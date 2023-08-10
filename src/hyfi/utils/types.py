from enum import Enum
from os import PathLike
from pathlib import PosixPath, WindowsPath
from typing import Dict, List, Mapping, Sequence, Union

from omegaconf import DictConfig, ListConfig

IntSeq = Sequence[int]
ListLike = (ListConfig, List, Sequence)
DictLike = (DictConfig, Dict, Mapping)
DictKeyType = Union[str, bytes, int, Enum, float, bool]
PathOrStr = Union[str, PathLike]
PathLikeType = Union[str, PosixPath, WindowsPath]

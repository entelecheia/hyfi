from .filter import DSFilter
from .load import DSLoad
from .process import DSProcess
from .save import DSSave
from .transform import DSTransform
from .types import DatasetDictType, DatasetLikeType, DatasetType
from .utils import DSUtils


class DATASETs(
    DSLoad,
    DSUtils,
    DSSave,
    DSFilter,
    DSTransform,
    DSProcess,
):
    def __init__(self):
        super().__init__()


__all__ = [
    "DSLoad",
    "DSUtils",
    "DatasetType",
    "DatasetDictType",
    "DatasetLikeType",
    "DATASETs",
]

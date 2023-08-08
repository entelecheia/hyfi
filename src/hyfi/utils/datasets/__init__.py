from .aggregate import DSAggregate
from .basic import DSBasic
from .combine import DSCombine
from .load import DSLoad
from .plot import DSPlot
from .reshape import DSReshape
from .save import DSSave
from .slice import DSSlice
from .types import DatasetDictType, DatasetLikeType, DatasetType
from .utils import DSUtils


class DATASETs(
    DSAggregate,
    DSBasic,
    DSCombine,
    DSLoad,
    DSPlot,
    DSReshape,
    DSSave,
    DSSlice,
    DSUtils,
):
    def __init__(self):
        super().__init__()


__all__ = [
    "DatasetDictType",
    "DatasetLikeType",
    "DATASETs",
    "DatasetType",
    "DSLoad",
    "DSUtils",
]

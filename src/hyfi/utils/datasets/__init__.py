"""
A collection of utility classes for working with datasets.

This module provides various classes for aggregating, combining, loading, plotting, reshaping, saving, slicing,
and performing other operations on datasets. It also defines some common types used in dataset operations.

Classes:
- DSAggregate: Class for aggregating datasets.
- DSBasic: Class for basic dataset operations.
- DSCombine: Class for combining datasets.
- DSLoad: Class for loading datasets.
- DSPlot: Class for plotting datasets.
- DSReshape: Class for reshaping datasets.
- DSSave: Class for saving datasets.
- DSSlice: Class for slicing datasets.
- DSUtils: Class for utility functions related to datasets.

Types:
- DatasetDictType: Type hint for a dictionary-like dataset.
- DatasetLikeType: Type hint for a dataset-like object.
- DatasetType: Type hint for a dataset.

Attributes:
- __all__: List of names to be exported when using 'from hyfi.utils.datasets import *'.

Usage:
```
from hyfi.utils.datasets import DATASETs

dataset_utils = DATASETs()
# Use the utility classes and functions for working with datasets
```
"""

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
    """
    A class representing a collection of datasets.

    This class inherits from various dataset utility classes and provides a convenient way to access and manipulate datasets.

    Attributes:
        None

    Methods:
        None
    """


__all__ = [
    "DatasetDictType",
    "DatasetLikeType",
    "DATASETs",
    "DatasetType",
    "DSLoad",
    "DSUtils",
]

"""
Type aliases for datasets.
"""
from typing import Union

from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict, IterableDatasetDict
from datasets.iterable_dataset import IterableDataset

DatasetType = Union[Dataset, IterableDataset]
DatasetDictType = Union[DatasetDict, IterableDatasetDict]
DatasetLikeType = Union[
    Dataset,
    IterableDataset,
    DatasetDict,
    IterableDatasetDict,
]

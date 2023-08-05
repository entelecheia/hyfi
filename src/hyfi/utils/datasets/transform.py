from typing import Dict, List, Optional, Sequence, Union

import datasets as hfds
import pandas as pd
from datasets.arrow_dataset import Dataset
from datasets.info import DatasetInfo
from datasets.splits import NamedSplit

from hyfi.utils.logging import LOGGING

from .types import DatasetType

logger = LOGGING.getLogger(__name__)


class DSTransform:
    @staticmethod
    def concatenate_data(
        data: Union[Dict[str, pd.DataFrame], Sequence[pd.DataFrame], List[DatasetType]],
        columns: Optional[Sequence[str]] = None,
        add_split_key_column: bool = False,
        added_column_name: str = "_name_",
        ignore_index: bool = True,
        axis: int = 0,
        split: Optional[str] = None,
        verbose: bool = False,
        **kwargs,
    ) -> Union[pd.DataFrame, DatasetType]:
        # if data is a list of datasets, concatenate them
        if isinstance(data, list) and isinstance(data[0], Dataset):
            return DSTransform.concatenate_datasets(
                data,
                axis=axis,
                split=split,
                **kwargs,
            )
        else:
            return DSTransform.concatenate_dataframes(
                data,
                columns=columns,
                add_split_key_column=add_split_key_column,
                added_column_name=added_column_name,
                ignore_index=ignore_index,
                axis=axis,
                verbose=verbose,
                **kwargs,
            )

    @staticmethod
    def concatenate_dataframes(
        data: Union[Dict[str, pd.DataFrame], Sequence[pd.DataFrame]],
        columns: Optional[Sequence[str]] = None,
        add_split_key_column: bool = False,
        added_column_name: str = "_name_",
        ignore_index: bool = True,
        axis: int = 0,
        verbose: bool = False,
        **kwargs,
    ) -> pd.DataFrame:
        """Concatenate dataframes"""
        if isinstance(data, dict):
            dfs = []
            for split in data:
                df = data[split]
                if add_split_key_column:
                    df[added_column_name] = split
                dfs.append(df)
            data = dfs
        if add_split_key_column:
            columns.append(added_column_name)
        if isinstance(data, list):
            if isinstance(columns, list):
                _columns = [c for c in columns if c in df.columns]
                data = [df[_columns] for df in data]
            if verbose:
                logger.info("Concatenating %s dataframes", len(data))
            if len(data) > 0:
                return pd.concat(data, ignore_index=ignore_index, axis=axis)
            else:
                raise ValueError("No dataframes to concatenate")
        else:
            logger.warning("Warning: data is not a dict")
            return data

    @staticmethod
    def concatenate_datasets(
        dsets: List[DatasetType],
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        axis: int = 0,
    ) -> DatasetType:
        """
        Converts a list of [`Dataset`] with the same schema into a single [`Dataset`].

        Args:
            dsets (`List[datasets.Dataset]`):
                List of Datasets to concatenate.
            info (`DatasetInfo`, *optional*):
                Dataset information, like description, citation, etc.
            split (`NamedSplit`, *optional*):
                Name of the dataset split.
            axis (`{0, 1}`, defaults to `0`):
                Axis to concatenate over, where `0` means over rows (vertically) and `1` means over columns
                (horizontally).

                <Added version="1.6.0"/>

        Example:

        ```py
        >>> ds3 = concatenate_datasets([ds1, ds2])
        ```
        """
        return hfds.concatenate_datasets(
            dsets=dsets,
            info=info,
            split=split,
            axis=axis,
        )

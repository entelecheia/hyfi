"""
Filter datasets. Slice, sample, and filter datasets.
"""
import random
from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd
from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict
from datasets.splits import Split

from hyfi.utils.logging import LOGGING

from .save import DSSave
from .types import DatasetLikeType

logger = LOGGING.getLogger(__name__)


class DSSlice:
    @staticmethod
    def sample_dataset(
        data: DatasetLikeType,
        split: Optional[Union[str, Split]] = None,
        sample_size: Union[int, float] = 100,
        sample_seed: int = 42,
        randomize: bool = True,
        num_heads: Optional[int] = 1,
        num_tails: Optional[int] = 1,
        verbose: bool = False,
    ) -> Dataset:
        """Sample a dataset."""
        if not isinstance(data, Dataset or DatasetDict):
            if split is None:
                raise ValueError(
                    "Please provide a split name when sampling a DatasetDict."
                )
            data = data[split]
        if sample_seed > 0:
            random.seed(sample_seed)
        if sample_size < 1:
            sample_size = int(len(data) * sample_size)
        if randomize:
            idx = random.sample(range(len(data)), sample_size)
        else:
            idx = range(sample_size)

        data = data.select(idx)
        logger.info("Sampling done.")
        if verbose:
            if num_heads:
                num_heads = min(num_heads, len(data))
                print(data[:num_heads])
            if num_tails:
                num_tails = min(num_tails, len(data))
                print(data[-num_tails:])

        return data

    @staticmethod
    def filter_and_sample_data(
        data: pd.DataFrame,
        queries: Optional[Union[str, List[str]]] = None,
        sample_size: Optional[Union[int, float]] = None,
        sample_seed: int = 42,
        output_dir: str = ".",
        sample_filename: Optional[str] = None,
        train_filename: Optional[str] = "train.parquet",
        discard_filename: Optional[str] = None,
        returning_data: str = "train",
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Filter the data to remove short documents and create a sample for analysis

        Args:
            data (pd.DataFrame): The data to filter and sample
            queries (Optional[Union[str, List[str]]], optional): The queries to filter by. Defaults to None.
            sample_size (Optional[Union[int, float]], optional): The sample size. Defaults to None.
            sample_seed (int, optional): The seed for sampling. Defaults to 42.
            output_dir (str, optional): The output directory. Defaults to ".".
            sample_filename (Optional[str], optional): The sample filename. Defaults to None.
            train_filename (Optional[str], optional): The train filename. Defaults to "train.parquet".
            discard_filename (Optional[str], optional): The discard filename. Defaults to "discard.parquet".
            returning_data (str, optional): The data to return. Defaults to "train" ('train', 'sample', 'discard', or 'original').
            verbose (bool, optional): Whether to print the sample. Defaults to False.

        Returns:
            pd.DataFrame: The original data
        """
        # Filter by queries
        if queries:
            data_ = DSSlice.filter_data_by_queries(
                data.copy(), queries, verbose=verbose
            )
        else:
            logger.warning("No query specified")
            data_ = data.copy()

        # Create a sample for analysis
        sample = None
        if sample_size:
            sample = DSSlice.sample_data(
                data_,
                sample_size_per_group=sample_size,
                sample_seed=sample_seed,
                verbose=verbose,
            )
            if sample_filename:
                DSSave.save_dataframes(
                    sample,
                    data_file=f"{output_dir}/{sample_filename}",
                    verbose=verbose,
                )
            if verbose:
                print(sample.head())

        # Create a train set
        train = data_[~data_.index.isin(sample.index)] if sample is not None else data_
        if train_filename:
            DSSave.save_dataframes(
                train,
                data_file=f"{output_dir}/{train_filename}",
                verbose=verbose,
            )
        if verbose:
            print(train.head())

        # Create a discard set
        if sample is not None:
            discard = data[
                ~data.index.isin(train.index) & ~data.index.isin(sample.index)
            ]
        else:
            discard = data[~data.index.isin(train.index)]
        if discard_filename:
            DSSave.save_dataframes(
                discard,
                data_file=f"{output_dir}/{discard_filename}",
                verbose=verbose,
            )
        if verbose:
            print(discard.head())
        logger.info(
            "Created %d samples, %d train samples, and %d discard samples",
            sample.shape[0] if sample is not None else 0,
            train.shape[0],
            discard.shape[0],
        )

        if returning_data == "train":
            return train
        elif returning_data == "sample" and sample is not None:
            return sample
        elif returning_data == "discard":
            return discard
        return data

    @staticmethod
    def filter_data_by_queries(
        data: pd.DataFrame,
        queries: Union[str, List[str]],
        verbose=False,
    ) -> pd.DataFrame:
        """
        Filter the data by queries

        Args:
            data: The data to filter
            queries: The queries to filter the data by
            verbose: Whether to print verbose logs

        Returns:
            The filtered data

        Examples:
            >>> import pandas as pd
            >>> data = pd.DataFrame({"text": ["hello world", "hello", "world"]})
            >>> filter_by_queries(data, "text.str.split().str.len() >= 2")
                text
            0  hello world
            >>> filter_by_queries(data, ["text.str.contains('hello')", "text.str.contains('world')"])
                text
            0  hello world
            2        world
        """
        if isinstance(queries, str):
            queries = [queries]

        for qry in queries:
            logger.info("filtering data by %s", qry)
            n_docs = data.shape[0]
            data = data.query(qry, engine="python")
            if verbose:
                logger.info("filtered %d documents", n_docs - data.shape[0])
        return data

    @staticmethod
    def sample_data(
        data: pd.DataFrame,
        sample_size_per_group: Union[float, int],
        sample_seed: int = 123,
        group_by: Optional[str] = None,
        value_col: Optional[str] = None,
        remove_columns: Optional[List[str]] = None,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Sample data from a dataframe

        Args:
            data: The dataframe to sample from
            sample_size_per_group: The number or fraction of samples to take from each group
            sample_seed: Random seed for sampling
            group_by: Column to group the data by, default is None (no grouping)
            value_col: Column containing the value to sample by, default is None (only for grouped sampling to count the number of samples per group)
            remove_columns: Columns to remove from sampled dataframe, default is None (keep all columns)
            verbose: Print verbose logs

        Returns:
            The sampled dataframe

        Examples:
            >>> import pandas as pd
            >>> data = pd.DataFrame({"text": ["hello world", "hello", "world"]})
            >>> sample_data(data, 1)
                text
            0  hello world
        """
        if verbose:
            logger.info("Sampling data")

        if not group_by:
            _sample = (
                data.sample(frac=sample_size_per_group, random_state=sample_seed)
                if sample_size_per_group < 1
                else data.sample(n=sample_size_per_group, random_state=sample_seed)
            )
        elif sample_size_per_group < 1:
            _sample = data.groupby(group_by, group_keys=False).apply(
                lambda x: x.sample(frac=sample_size_per_group, random_state=sample_seed)
            )
        else:
            _sample = data.groupby(group_by, group_keys=False).apply(
                lambda x: x.sample(
                    n=min(len(x), sample_size_per_group), random_state=sample_seed
                )
            )
        _sample.reset_index(drop=True, inplace=True)
        if remove_columns:
            logger.info("Removing columns: %s", remove_columns)
            _sample = _sample.drop(columns=remove_columns)
        if verbose:
            logger.info("Total rows in data: %s", len(data))
            logger.info("Total rows in sample: %s", len(_sample))
            print(_sample.head())

            if group_by and value_col:
                grp_all = data.groupby(group_by)[value_col].count().rename("population")
                grp_sample = (
                    _sample.groupby(group_by)[value_col].count().rename("sample")
                )
                grp_dists = pd.concat([grp_all, grp_sample], axis=1)
                print(grp_dists)

        return _sample

    @staticmethod
    def split_dataframe(
        data,
        indices_or_sections: Union[int, Sequence[int]],
        verbose: bool = False,
    ) -> List[pd.DataFrame]:
        """
        Split a dataframe into multiple dataframes

        Args:
            data (pd.DataFrame): dataframe to split
            indices_or_sections (int or sequence of ints): if int, number of chunks to split the dataframe into

        Returns:
            List[pd.DataFrame]: list of dataframes

        Examples:
            >>> import pandas as pd
            >>> data = pd.DataFrame({"text": ["hello world", "hello", "world"]})
            >>> split_dataframe(data, 2)
            [        text
            0  hello world,
            1        hello,        text
            2  world]

        """

        if verbose:
            logger.info("Splitting dataframe into %s", indices_or_sections)
        return np.array_split(data, indices_or_sections)

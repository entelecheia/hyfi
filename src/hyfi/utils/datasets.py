import os
import random
from os import PathLike
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

import datasets as hfds
import pandas as pd
from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict, IterableDatasetDict
from datasets.download.download_config import DownloadConfig
from datasets.download.download_manager import DownloadMode
from datasets.features import Features
from datasets.info import DatasetInfo
from datasets.iterable_dataset import IterableDataset
from datasets.splits import NamedSplit, Split
from datasets.utils.info_utils import VerificationMode

from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

DatasetType = Union[Dataset, IterableDataset]
DatasetDictType = Union[DatasetDict, IterableDatasetDict]
DatasetLikeType = Union[
    Dataset,
    IterableDataset,
    DatasetDict,
    IterableDatasetDict,
]


class DATASETs:
    @staticmethod
    def is_dataframe(data: Any) -> bool:
        """Check if data is a pandas dataframe"""
        return isinstance(data, pd.DataFrame)

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
            return DATASETs.concatenate_datasets(
                data,
                axis=axis,
                split=split,
                **kwargs,
            )
        else:
            return DATASETs.concatenate_dataframes(
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
    def load_data(
        path: Optional[str] = "pandas",
        name: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, Sequence[str]]] = None,
        split: Optional[str] = "train",
        filetype: Optional[str] = None,
        concatenate: Optional[bool] = False,
        use_cached: bool = False,
        verbose: Optional[bool] = False,
        **kwargs,
    ) -> Union[Dict[str, pd.DataFrame], Dict[str, DatasetType]]:
        """Load data from a file or a list of files"""
        if path in ["dataframe", "df", "pandas"]:
            data = DATASETs.load_dataframes(
                data_files,
                data_dir=data_dir,
                filetype=filetype,
                split=split,
                concatenate=concatenate,
                use_cached=use_cached,
                verbose=verbose,
                **kwargs,
            )
            if data is not None:
                return data if isinstance(data, dict) else {split: data}
            else:
                return {}
        else:
            dset = DATASETs.load_dataset(
                path,
                name=name,
                data_dir=data_dir,
                data_files=data_files,
                split=split,
                **kwargs,
            )
            split = split or "train"
            if isinstance(dset, (Dataset, IterableDataset)):
                return {split: dset}
            if concatenate:
                return {split: DATASETs.concatenate_datasets(dset.values())}
            else:
                return {k: v for k, v in dset.items() if v is not None}

    @staticmethod
    def get_data_files(
        data_files: Optional[
            Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]
        ] = None,
        data_dir: Optional[str] = None,
        split: Optional[str] = None,
        recursive: bool = True,
        use_cached: bool = False,
        verbose: bool = False,
        **kwargs,
    ) -> Union[List[str], Dict[str, List[str]]]:
        if isinstance(data_files, dict):
            return {
                name: IOLIBs.get_filepaths(
                    files,
                    data_dir,
                    recursive=recursive,
                    use_cached=use_cached,
                    verbose=verbose,
                    **kwargs,
                )
                for name, files in data_files.items()
            }
        filepaths = IOLIBs.get_filepaths(
            data_files,
            data_dir,
            recursive=recursive,
            use_cached=use_cached,
            verbose=verbose,
            **kwargs,
        )
        return {split: filepaths} if split else filepaths

    @staticmethod
    def load_dataframes(
        data_files: Union[str, Sequence[str]],
        data_dir: Optional[str] = None,
        filetype: Optional[str] = None,
        split: Optional[str] = None,
        concatenate: bool = False,
        ignore_index: bool = False,
        use_cached: bool = False,
        verbose: bool = False,
        **kwargs,
    ) -> Optional[Union[Dict[str, pd.DataFrame], pd.DataFrame]]:
        """Load data from a file or a list of files"""
        if not data_files:
            logger.warning("No data_files provided")
            return {}

        filepaths = DATASETs.get_data_files(
            data_files,
            data_dir,
            split=split,
            use_cached=use_cached,
            verbose=verbose,
            **kwargs,
        )

        if isinstance(filepaths, dict):
            data = {
                name: pd.concat(
                    [
                        DATASETs.load_dataframe(
                            f, verbose=verbose, filetype=filetype, **kwargs
                        )
                        for f in files
                    ],
                    ignore_index=ignore_index,
                )
                for name, files in filepaths.items()
            }
            data = {k: v for k, v in data.items() if v is not None}
            return data
        else:
            data = {
                os.path.basename(f): DATASETs.load_dataframe(
                    f, verbose=verbose, filetype=filetype, **kwargs
                )
                for f in filepaths
            }
            data = {k: v for k, v in data.items() if v is not None}
            if len(data) == 1:
                data = list(data.values())[0]
            elif len(data) > 1:
                if concatenate or split:
                    data = pd.concat(data.values(), ignore_index=ignore_index)
            else:
                logger.warning(f"No files found for {data_files}")
                return None
            return {split: data} if split else data

    @staticmethod
    def load_dataframe(
        data_file: str,
        data_dir: Optional[str] = None,
        filetype: Optional[str] = None,
        columns: Optional[Sequence[str]] = None,
        index_col: Union[str, int, Sequence[str], Sequence[int], None] = None,
        verbose: bool = False,
        **kwargs,
    ) -> pd.DataFrame:
        """Load a dataframe from a file"""
        dtype = kwargs.pop("dtype", None)
        if isinstance(dtype, list):
            dtype = {k: "str" for k in dtype}
        parse_dates = kwargs.pop("parse_dates", False)

        if data_file.startswith("http"):
            filepath = data_file
        else:
            filepath = os.path.join(data_dir, data_file) if data_dir else data_file
            if not os.path.exists(filepath):
                logger.warning(f"File {filepath} does not exist")
                raise FileNotFoundError(f"File {filepath} does not exist")
        filetype = (
            data_file.split(".")[-1]
            if data_file.split(".")[-1] in ["csv", "tsv", "parquet"]
            else filetype
        )
        filetype = filetype or "csv"
        filetype = filetype.replace(".", "")
        if filetype not in ["csv", "tsv", "parquet"]:
            raise ValueError("`file` should be a csv or a parquet file.")
        if verbose:
            logger.info(f"Loading data from {filepath}")
        with elapsed_timer(format_time=True) as elapsed:
            if "csv" in filetype or "tsv" in filetype:
                delimiter = kwargs.pop("delimiter", "\t") if "tsv" in filetype else None
                data = pd.read_csv(
                    filepath,
                    index_col=index_col,
                    dtype=dtype,
                    parse_dates=parse_dates,
                    delimiter=delimiter,
                )
            elif "parquet" in filetype:
                engine = kwargs.pop("engine", "pyarrow")
                if engine not in ["pyarrow", "fastparquet"]:
                    engine = "auto"
                data = pd.read_parquet(filepath, engine=engine)  # type: ignore
            else:
                raise ValueError("filetype must be .csv or .parquet")
            if isinstance(columns, list):
                columns = [c for c in columns if c in data.columns]
                data = data[columns]
            if verbose:
                logger.info(" >> elapsed time to load data: %s", elapsed())
        return data

    @staticmethod
    def save_dataframes(
        data: Union[pd.DataFrame, dict],
        data_file: str,
        data_dir: Optional[str] = None,
        columns: Optional[Sequence[str]] = None,
        index: bool = False,
        filetype: Optional[str] = "parquet",
        suffix: Optional[str] = None,
        verbose: bool = False,
        **kwargs,
    ):
        """Save data to a file"""
        if data_file is None:
            raise ValueError("filename must be specified")
        fileinfo = os.path.splitext(data_file)
        data_file = fileinfo[0]
        filetype = fileinfo[1] if len(fileinfo) > 1 else filetype
        filetype = "." + filetype.replace(".", "")
        if suffix:
            data_file = f"{data_file}-{suffix}{filetype}"
        else:
            data_file = f"{data_file}{filetype}"
        filepath = os.path.join(data_dir, data_file) if data_dir else data_file
        data_dir = os.path.dirname(filepath)
        data_file = os.path.basename(filepath)
        os.makedirs(data_dir, exist_ok=True)

        if isinstance(data, dict):
            for k, v in data.items():
                DATASETs.save_dataframes(
                    v,
                    data_file,
                    data_dir=data_dir,
                    columns=columns,
                    index=index,
                    filetype=filetype,
                    suffix=k,
                    verbose=verbose,
                    **kwargs,
                )
        elif DATASETs.is_dataframe(data):
            logger.info("Saving dataframe to %s", Path(filepath).absolute())
            if isinstance(columns, list):
                columns = [c for c in columns if c in data.columns]
                data = data[columns]
            with elapsed_timer(format_time=True) as elapsed:
                if "csv" in filetype or "tsv" in filetype:
                    data.to_csv(filepath, index=index)
                elif "parquet" in filetype:
                    compression = kwargs.get("compression", "gzip")
                    engine = kwargs.get("engine", "pyarrow")
                    if engine not in ["pyarrow", "fastparquet"]:
                        engine = "auto"
                    data.to_parquet(filepath, compression=compression, engine=engine)  # type: ignore
                else:
                    raise ValueError("filetype must be .csv or .parquet")
                if verbose:
                    logger.info(" >> elapsed time to save data: %s", elapsed())
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    @staticmethod
    def to_datetime(
        data,
        _format: Optional[str] = None,
        _columns: Optional[Union[str, Sequence[str]]] = None,
        **kwargs,
    ):
        """Convert a string, int, or datetime object to a datetime object"""
        from datetime import datetime

        import pandas as pd

        if isinstance(data, datetime):
            return data
        elif isinstance(data, str):
            if _format is None:
                _format = "%Y-%m-%d"
            return datetime.strptime(data, _format)
        elif isinstance(data, int):
            return datetime.fromtimestamp(data)
        elif isinstance(data, pd.DataFrame):
            if _columns:
                if isinstance(_columns, str):
                    _columns = [_columns]
                for _col in _columns:
                    data[_col] = pd.to_datetime(data[_col], format=_format, **kwargs)
            return data
        else:
            return data

    @staticmethod
    def to_numeric(
        data,
        _columns: Optional[Union[str, Sequence[str]]] = None,
        errors: Optional[str] = "coerce",
        downcast: Optional[str] = None,
        **kwargs,
    ):
        """Convert a string, int, or float object to a float object"""
        import pandas as pd

        if isinstance(data, str):
            return float(data)
        elif isinstance(data, (int, float)) or not isinstance(data, pd.DataFrame):
            return data
        else:
            if _columns:
                if isinstance(_columns, str):
                    _columns = [_columns]
                for _col in _columns:
                    data[_col] = pd.to_numeric(data[_col], errors=errors, downcast=downcast)  # type: ignore
            return data

    @staticmethod
    def dict_to_dataframe(
        data: Dict[Any, Any],
        orient: str = "columns",
        dtype=None,
        columns=None,
    ) -> pd.DataFrame:
        """Convert a dictionary to a pandas dataframe"""
        import pandas as pd

        return pd.DataFrame.from_dict(data, orient=orient, dtype=dtype, columns=columns)  # type: ignore

    @staticmethod
    def records_to_dataframe(
        data,
        index=None,
        exclude=None,
        columns=None,
        coerce_float=False,
        nrows=None,
    ) -> pd.DataFrame:
        """Convert a list of records to a pandas dataframe"""
        import pandas as pd

        return pd.DataFrame.from_records(
            data,
            index=index,
            exclude=exclude,
            columns=columns,
            coerce_float=coerce_float,
            nrows=nrows,
        )

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

    @staticmethod
    def load_dataset(
        path: str,
        name: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[
            Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]
        ] = None,
        split: Optional[Union[str, Split]] = None,
        cache_dir: Optional[str] = None,
        features: Optional[Features] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[Union[DownloadMode, str]] = None,
        verification_mode: Optional[Union[VerificationMode, str]] = None,
        num_proc: Optional[int] = None,
        **config_kwargs,
    ) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        """Load a dataset from the Hugging Face Hub, or a local dataset.

        You can find the list of datasets on the [Hub](https://huggingface.co/datasets) or with [`datasets.list_datasets`].

        A dataset is a directory that contains:

        - some data files in generic formats (JSON, CSV, Parquet, text, etc.).
        - and optionally a dataset script, if it requires some code to read the data files. This is used to load any kind of formats or structures.

         Returns:
            [`Dataset`] or [`DatasetDict`]:
            - if `split` is not `None`: the dataset requested,
            - if `split` is `None`, a [`~datasets.DatasetDict`] with each split.

            or [`IterableDataset`] or [`IterableDatasetDict`]: if `streaming=True`

            - if `split` is not `None`, the dataset is requested
            - if `split` is `None`, a [`~datasets.streaming.IterableDatasetDict`] with each split.

        """
        return hfds.load_dataset(
            path=path,
            name=name,
            data_dir=data_dir,
            data_files=data_files,
            split=split,
            cache_dir=cache_dir,
            features=features,
            download_config=download_config,
            download_mode=download_mode,
            verification_mode=verification_mode,
            num_proc=num_proc,
            **config_kwargs,
        )

    @staticmethod
    def load_dataset_from_disk(
        dataset_path: str,
        keep_in_memory: Optional[bool] = None,
        storage_options: Optional[dict] = None,
        num_heads: Optional[int] = 1,
        num_tails: Optional[int] = 1,
        verbose: bool = False,
    ) -> Union[Dataset, DatasetDict]:
        """Load a dataset from the filesystem."""
        data = hfds.load_from_disk(
            dataset_path=dataset_path,
            keep_in_memory=keep_in_memory,
            storage_options=storage_options,
        )
        logger.info("Dataset loaded from %s.", dataset_path)
        if verbose:
            if isinstance(data, DatasetDict or IterableDatasetDict):
                for split in data:
                    logger.info("Split: %s", split)
                    logger.info("Dataset features: %s", data[split].features)
                    logger.info("Number of records: %s", len(data[split]))
            else:
                if num_heads:
                    num_heads = min(num_heads, len(data))
                    print(data[:num_heads])
                if num_tails:
                    num_tails = min(num_tails, len(data))
                    print(data[-num_tails:])
                logger.info("Dataset features: %s", data.features)
                logger.info("Number of records: %s", len(data))

        return data

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
    def save_dataset_to_disk(
        dset: DatasetLikeType,
        dataset_path: PathLike,
        max_shard_size: Optional[Union[str, int]] = None,
        num_shards: Optional[int] = None,
        num_proc: Optional[int] = None,
        storage_options: Optional[dict] = None,
        verbose: bool = False,
        **kwargs,
    ) -> DatasetLikeType:
        """Save a dataset or a dataset dict to the filesystem."""
        dset.save_to_disk(
            dataset_path,
            max_shard_size=max_shard_size,
            num_shards=num_shards,
            num_proc=num_proc,
            storage_options=storage_options,
        )
        logger.info("Dataset saved to %s.", dataset_path)
        if verbose:
            if isinstance(dset, DatasetDict or IterableDatasetDict):
                for split in dset:
                    logger.info("Split: %s", split)
                    logger.info("Dataset features: %s", dset[split].features)
                    logger.info("Number of records: %s", len(dset[split]))
            else:
                logger.info("Dataset features: %s", dset.features)
                logger.info("Number of records: %s", len(dset))

        return dset

    @staticmethod
    def filter_and_sample_data(
        data: pd.DataFrame,
        queries: Optional[Union[str, List[str]]] = None,
        sample_size: Optional[Union[int, float]] = None,
        sample_seed: int = 42,
        output_dir: str = ".",
        sample_filename: Optional[str] = None,
        train_filename: Optional[str] = "train.parquet",
        discard_filename: Optional[str] = "discard.parquet",
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Filter the data to remove short documents and create a sample for analysis
        """
        # Filter by queries
        if queries:
            data_ = DATASETs.filter_data_by_queries(data, queries, verbose=verbose)
        else:
            logger.warning("No query specified")
            data_ = data.copy()

        # Create a sample for analysis
        sample = None
        if sample_size:
            sample = DATASETs.sample_data(
                data_,
                sample_size_per_group=sample_size,
                sample_seed=sample_seed,
                verbose=verbose,
            )
            if sample_filename:
                DATASETs.save_dataframes(
                    sample,
                    data_file=f"{output_dir}/{sample_filename}",
                    verbose=verbose,
                )
            if verbose:
                print(sample.head())

        # Create a train set
        train = data_[~data_.index.isin(sample.index)] if sample is not None else data_
        if train_filename:
            DATASETs.save_dataframes(
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
            DATASETs.save_dataframes(
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

        return train

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

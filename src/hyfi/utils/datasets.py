import os
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
DatasetLikeType = Union[Dataset, IterableDataset, DatasetDict, IterableDatasetDict]


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
        data_dir: Optional[str] = "",
        data_files: Optional[Union[str, Sequence[str]]] = None,
        split: Optional[str] = "train",
        filetype: Optional[str] = "",
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
        split: str = "",
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
        data_dir: str = "",
        filetype: str = "",
        split: str = "",
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
        data_dir: str = "",
        filetype: str = "parquet",
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
        data_dir: str = "",
        columns: Optional[Sequence[str]] = None,
        index: bool = False,
        filetype: str = "parquet",
        suffix: str = "",
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
    def to_datetime(data, _format=None, _columns=None, **kwargs):
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
        _columns=None,
        errors="coerce",
        downcast=None,
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
        data,
        orient="columns",
        dtype=None,
        columns=None,
    ):
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
    ):
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
    def save_to_disk(
        dset,
        dataset_path: PathLike,
        max_shard_size: Optional[Union[str, int]] = None,
        num_shards: Optional[int] = None,
        num_proc: Optional[int] = None,
        storage_options: Optional[dict] = None,
    ):
        dset.save_to_disk(
            dataset_path=dataset_path,
            max_shard_size=max_shard_size,
            num_shards=num_shards,
            num_proc=num_proc,
            storage_options=storage_options,
        )

    @staticmethod
    def load_from_disk(
        dataset_path: str,
        keep_in_memory: Optional[bool] = None,
        storage_options: Optional[dict] = None,
    ) -> Union[Dataset, DatasetDict]:
        return hfds.load_from_disk(
            dataset_path=dataset_path,
            keep_in_memory=keep_in_memory,
            storage_options=storage_options,
        )

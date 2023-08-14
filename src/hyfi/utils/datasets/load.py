"""
Load data from a file or a list of files
"""
import os
from pathlib import Path
from typing import Dict, Mapping, Optional, Sequence, Union

import datasets as hfds
import pandas as pd
from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict, IterableDatasetDict
from datasets.download.download_config import DownloadConfig
from datasets.download.download_manager import DownloadMode
from datasets.features import Features
from datasets.iterable_dataset import IterableDataset
from datasets.splits import Split
from datasets.utils.info_utils import VerificationMode

from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING

from .types import DatasetType
from .utils import DSUtils

logger = LOGGING.getLogger(__name__)


class DSLoad:
    def __init__(self):
        pass

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
            data = DSLoad.load_dataframes(
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
            dset = DSLoad.load_dataset(
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
                return {split: hfds.concatenate_datasets(dset.values())}
            else:
                return {k: v for k, v in dset.items() if v is not None}

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

        filepaths = DSUtils.get_data_files(
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
                        DSLoad.load_dataframe(
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
                os.path.basename(f): DSLoad.load_dataframe(
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
        data_file: Union[str, Path],
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

        data_file = str(data_file)
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

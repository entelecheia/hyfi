import os
from os import PathLike
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

import datasets as hfds
import pandas as pd
from datasets import Dataset
from datasets.dataset_dict import DatasetDict, IterableDatasetDict
from datasets.download.download_config import DownloadConfig
from datasets.download.download_manager import DownloadMode
from datasets.features import Features
from datasets.info import DatasetInfo
from datasets.iterable_dataset import IterableDataset
from datasets.splits import NamedSplit, Split
from datasets.tasks import TaskTemplate
from datasets.utils.info_utils import VerificationMode
from datasets.utils.version import Version

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
    ) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
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
        ignore_verifications="deprecated",
        keep_in_memory: Optional[bool] = None,
        save_infos: bool = False,
        revision: Optional[Union[str, Version]] = None,
        use_auth_token: Optional[Union[bool, str]] = None,
        task: Optional[Union[str, TaskTemplate]] = None,
        streaming: bool = False,
        num_proc: Optional[int] = None,
        storage_options: Optional[Dict] = None,
        **config_kwargs,
    ) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        """Load a dataset from the Hugging Face Hub, or a local dataset.

        You can find the list of datasets on the [Hub](https://huggingface.co/datasets) or with [`datasets.list_datasets`].

        A dataset is a directory that contains:

        - some data files in generic formats (JSON, CSV, Parquet, text, etc.).
        - and optionally a dataset script, if it requires some code to read the data files. This is used to load any kind of formats or structures.

        Note that dataset scripts can also download and read data files from anywhere - in case your data files already exist online.

        This function does the following under the hood:

            1. Download and import in the library the dataset script from `path` if it's not already cached inside the library.

                If the dataset has no dataset script, then a generic dataset script is imported instead (JSON, CSV, Parquet, text, etc.)

                Dataset scripts are small python scripts that define dataset builders. They define the citation, info and format of the dataset,
                contain the path or URL to the original data files and the code to load examples from the original data files.

                You can find the complete list of datasets in the Datasets [Hub](https://huggingface.co/datasets).

            2. Run the dataset script which will:

                * Download the dataset file from the original URL (see the script) if it's not already available locally or cached.
                * Process and cache the dataset in typed Arrow tables for caching.

                    Arrow table are arbitrarily long, typed tables which can store nested objects and be mapped to numpy/pandas/python generic types.
                    They can be directly accessed from disk, loaded in RAM or even streamed over the web.

            3. Return a dataset built from the requested splits in `split` (default: all).

        It also allows to load a dataset from a local directory or a dataset repository on the Hugging Face Hub without dataset script.
        In this case, it automatically loads all the data files from the directory or the dataset repository.

        Args:

            path (`str`):
                Path or name of the dataset.
                Depending on `path`, the dataset builder that is used comes from a generic dataset script (JSON, CSV, Parquet, text etc.) or from the dataset script (a python file) inside the dataset directory.

                For local datasets:

                - if `path` is a local directory (containing data files only)
                -> load a generic dataset builder (csv, json, text etc.) based on the content of the directory
                e.g. `'./path/to/directory/with/my/csv/data'`.
                - if `path` is a local dataset script or a directory containing a local dataset script (if the script has the same name as the directory)
                -> load the dataset builder from the dataset script
                e.g. `'./dataset/squad'` or `'./dataset/squad/squad.py'`.

                For datasets on the Hugging Face Hub (list all available datasets and ids with [`datasets.list_datasets`])

                - if `path` is a dataset repository on the HF hub (containing data files only)
                -> load a generic dataset builder (csv, text etc.) based on the content of the repository
                e.g. `'username/dataset_name'`, a dataset repository on the HF hub containing your data files.
                - if `path` is a dataset repository on the HF hub with a dataset script (if the script has the same name as the directory)
                -> load the dataset builder from the dataset script in the dataset repository
                e.g. `glue`, `squad`, `'username/dataset_name'`, a dataset repository on the HF hub containing a dataset script `'dataset_name.py'`.

            name (`str`, *optional*):
                Defining the name of the dataset configuration.
            data_dir (`str`, *optional*):
                Defining the `data_dir` of the dataset configuration. If specified for the generic builders (csv, text etc.) or the Hub datasets and `data_files` is `None`,
                the behavior is equal to passing `os.path.join(data_dir, **)` as `data_files` to reference all the files in a directory.
            data_files (`str` or `Sequence` or `Mapping`, *optional*):
                Path(s) to source data file(s).
            split (`Split` or `str`):
                Which split of the data to load.
                If `None`, will return a `dict` with all splits (typically `datasets.Split.TRAIN` and `datasets.Split.TEST`).
                If given, will return a single Dataset.
                Splits can be combined and specified like in tensorflow-datasets.
            cache_dir (`str`, *optional*):
                Directory to read/write data. Defaults to `"~/.cache/huggingface/datasets"`.
            features (`Features`, *optional*):
                Set the features type to use for this dataset.
            download_config ([`DownloadConfig`], *optional*):
                Specific download configuration parameters.
            download_mode ([`DownloadMode`] or `str`, defaults to `REUSE_DATASET_IF_EXISTS`):
                Download/generate mode.
            verification_mode ([`VerificationMode`] or `str`, defaults to `BASIC_CHECKS`):
                Verification mode determining the checks to run on the downloaded/processed dataset information (checksums/size/splits/...).

                <Added version="2.9.1"/>
            ignore_verifications (`bool`, defaults to `False`):
                Ignore the verifications of the downloaded/processed dataset information (checksums/size/splits/...).

                <Deprecated version="2.9.1">

                `ignore_verifications` was deprecated in version 2.9.1 and will be removed in 3.0.0.
                Please use `verification_mode` instead.

                </Deprecated>
            keep_in_memory (`bool`, defaults to `None`):
                Whether to copy the dataset in-memory. If `None`, the dataset
                will not be copied in-memory unless explicitly enabled by setting `datasets.config.IN_MEMORY_MAX_SIZE` to
                nonzero. See more details in the [improve performance](../cache#improve-performance) section.
            save_infos (`bool`, defaults to `False`):
                Save the dataset information (checksums/size/splits/...).
            revision ([`Version`] or `str`, *optional*):
                Version of the dataset script to load.
                As datasets have their own git repository on the Datasets Hub, the default version "main" corresponds to their "main" branch.
                You can specify a different version than the default "main" by using a commit SHA or a git tag of the dataset repository.
            use_auth_token (`str` or `bool`, *optional*):
                Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
                If `True`, or not specified, will get token from `"~/.huggingface"`.
            task (`str`):
                The task to prepare the dataset for during training and evaluation. Casts the dataset's [`Features`] to standardized column names and types as detailed in `datasets.tasks`.
            streaming (`bool`, defaults to `False`):
                If set to `True`, don't download the data files. Instead, it streams the data progressively while
                iterating on the dataset. An [`IterableDataset`] or [`IterableDatasetDict`] is returned instead in this case.

                Note that streaming works for datasets that use data formats that support being iterated over like txt, csv, jsonl for example.
                Json files may be downloaded completely. Also streaming from remote zip or gzip files is supported but other compressed formats
                like rar and xz are not yet supported. The tgz format doesn't allow streaming.
            num_proc (`int`, *optional*, defaults to `None`):
                Number of processes when downloading and generating the dataset locally.
                Multiprocessing is disabled by default.

                <Added version="2.7.0"/>
            storage_options (`dict`, *optional*, defaults to `None`):
                **Experimental**. Key/value pairs to be passed on to the dataset file-system backend, if any.

                <Added version="2.11.0"/>
            **config_kwargs (additional keyword arguments):
                Keyword arguments to be passed to the `BuilderConfig`
                and used in the [`DatasetBuilder`].

        Returns:
            [`Dataset`] or [`DatasetDict`]:
            - if `split` is not `None`: the dataset requested,
            - if `split` is `None`, a [`~datasets.DatasetDict`] with each split.

            or [`IterableDataset`] or [`IterableDatasetDict`]: if `streaming=True`

            - if `split` is not `None`, the dataset is requested
            - if `split` is `None`, a [`~datasets.streaming.IterableDatasetDict`] with each split.

        Example:

        Load a dataset from the Hugging Face Hub:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset('rotten_tomatoes', split='train')

        # Map data files to splits
        >>> data_files = {'train': 'train.csv', 'test': 'test.csv'}
        >>> ds = load_dataset('namespace/your_dataset_name', data_files=data_files)
        ```

        Load a local dataset:

        ```py
        # Load a CSV file
        >>> from datasets import load_dataset
        >>> ds = load_dataset('csv', data_files='path/to/local/my_dataset.csv')

        # Load a JSON file
        >>> from datasets import load_dataset
        >>> ds = load_dataset('json', data_files='path/to/local/my_dataset.json')

        # Load from a local loading script
        >>> from datasets import load_dataset
        >>> ds = load_dataset('path/to/local/loading_script/loading_script.py', split='train')
        ```

        Load an [`~datasets.IterableDataset`]:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset('rotten_tomatoes', split='train', streaming=True)
        ```

        Load an image dataset with the `ImageFolder` dataset builder:

        ```py
        >>> from datasets import load_dataset
        >>> ds = load_dataset('imagefolder', data_dir='/path/to/images', split='train')
        ```
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
            ignore_verifications=ignore_verifications,
            keep_in_memory=keep_in_memory,
            save_infos=save_infos,
            revision=revision,
            use_auth_token=use_auth_token,
            task=task,
            streaming=streaming,
            num_proc=num_proc,
            storage_options=storage_options,
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

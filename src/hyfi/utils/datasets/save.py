"""
Save datasets to disk
"""
import os
from os import PathLike
from pathlib import Path
from typing import Optional, Sequence, Union

import pandas as pd
from datasets.dataset_dict import DatasetDict, IterableDatasetDict

from hyfi.utils.contexts import elapsed_timer
from hyfi.utils.logging import LOGGING

from .types import DatasetLikeType
from .utils import DSUtils

logger = LOGGING.getLogger(__name__)


class DSSave:
    def __init__(self):
        pass

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
                DSSave.save_dataframes(
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
        elif DSUtils.is_dataframe(data):
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

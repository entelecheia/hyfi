"""
Dataset utilities
"""
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

import pandas as pd
from datasets.arrow_dataset import Dataset
from datasets.iterable_dataset import IterableDataset

from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class DSUtils:
    def __init__(self):
        pass

    @staticmethod
    def is_dataframe(data: Any) -> bool:
        """Check if data is a pandas dataframe"""
        return isinstance(data, pd.DataFrame)

    @staticmethod
    def is_dataset(data: Any) -> bool:
        """Check if data is a HuggingFace dataset"""
        return isinstance(data, Dataset or IterableDataset)

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

import os
from typing import Union

import pandas as pd

from hyfi.utils.file import get_filepaths
from hyfi.utils.func import elapsed_timer
from hyfi.utils.logging import getLogger

logger = getLogger(__name__)


def is_dataframe(data) -> bool:
    """Check if data is a pandas dataframe"""
    return isinstance(data, pd.DataFrame)


def concat_data(
    data,
    columns=None,
    add_key_as_name: bool = False,
    name_column: str = "_name_",
    ignore_index: bool = True,
    **kwargs,
):
    """Concatenate dataframes"""
    if isinstance(data, dict):
        logger.info(f"Concatenating {len(data)} dataframes")
        dfs = []
        for df_name in data:
            df_each = data[df_name]
            if isinstance(columns, list):
                _columns = [c for c in columns if c in df_each.columns]
                df_each = df_each[_columns]
            if add_key_as_name:
                df_each[name_column] = df_name
            dfs.append(df_each)
        return pd.concat(dfs, ignore_index=ignore_index) if dfs else None
    elif isinstance(data, list):
        logger.info(f"Concatenating {len(data)} dataframes")
        return pd.concat(data, ignore_index=ignore_index) if len(data) > 0 else None
    else:
        logger.warning("Warning: data is not a dict")
        return data


def load_data(
    filename,
    base_dir=None,
    filetype=None,
    verbose=False,
    **kwargs,
):
    """Load data from a file or a list of files"""
    concatenate = kwargs.pop("concatenate", False)
    ignore_index = kwargs.pop("ignore_index", False)
    if filename is not None:
        filename = str(filename)

    if filename.startswith("http"):
        if not filetype:
            filetype = filename.split(".")[-1]
        if filetype not in ["csv", "parquet"]:
            raise ValueError("`file` should be a csv or a parquet file.")
        kwargs["filetype"] = filetype
        return load_dataframe(filename, verbose=verbose, **kwargs)

    if base_dir:
        filepaths = get_filepaths(filename, base_dir)
    else:
        filepaths = get_filepaths(filename)
    if verbose:
        logger.info(f"Loading {len(filepaths)} dataframes from {filepaths}")

    data = {
        os.path.basename(f): load_dataframe(
            f, verbose=verbose, filetype=filetype, **kwargs
        )
        for f in filepaths
    }
    data = {k: v for k, v in data.items() if v is not None}
    if len(data) == 1:
        return list(data.values())[0]
    elif len(filepaths) > 1:
        if concatenate:
            return pd.concat(data.values(), ignore_index=ignore_index)
        else:
            return data
    else:
        logger.warning(f"No files found for {filename}")
        return None


def load_dataframe(
    filename: str,
    base_dir: str = "",
    columns: list = None,  # type: ignore
    index_col=None,
    verbose: bool = False,
    **kwargs,
) -> Union[pd.DataFrame, None]:
    """Load a dataframe from a file"""
    dtype = kwargs.pop("dtype", None)
    if isinstance(dtype, list):
        dtype = {k: "str" for k in dtype}
    parse_dates = kwargs.pop("parse_dates", False)

    filetype = kwargs.pop("filetype", None) or "parquet"
    if filename.startswith("http"):
        filepath = filename
    else:
        fileinfo = os.path.splitext(filename)
        filename = fileinfo[0]
        filetype = fileinfo[1] if len(fileinfo) > 1 else filetype
        filetype = "." + filetype.replace(".", "")
        filename = f"{filename}{filetype}"
        filepath = os.path.join(base_dir, filename) if base_dir else filename
        if not os.path.exists(filepath):
            logger.warning(f"File {filepath} does not exist")
            return None
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


def save_data(
    data: Union[pd.DataFrame, dict],
    filename: str,
    base_dir: str = "",
    columns=None,
    index: bool = False,
    filetype="parquet",
    suffix: str = "",
    verbose: bool = False,
    **kwargs,
):
    """Save data to a file"""
    if filename is None:
        raise ValueError("filename must be specified")
    fileinfo = os.path.splitext(filename)
    filename = fileinfo[0]
    filetype = fileinfo[1] if len(fileinfo) > 1 else filetype
    filetype = "." + filetype.replace(".", "")
    if suffix:
        filename = f"{filename}-{suffix}{filetype}"
    else:
        filename = f"{filename}{filetype}"
    filepath = os.path.join(base_dir, filename) if base_dir else filename
    base_dir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    os.makedirs(base_dir, exist_ok=True)

    if isinstance(data, dict):
        for k, v in data.items():
            save_data(
                v,
                filename,
                base_dir=base_dir,
                columns=columns,
                index=index,
                filetype=filetype,
                suffix=k,
                verbose=verbose,
                **kwargs,
            )
    elif is_dataframe(data):
        logger.info("Saving dataframe to %s", filepath)
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

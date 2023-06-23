"""
    This module contains the primary class for the hyfi config package, HyFI,
    as well as various utility functions and imports.
"""
import os
from pathlib import Path, PosixPath, WindowsPath
from typing import (
    IO,
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import pandas as pd
from omegaconf import DictConfig, ListConfig, SCMode

from hyfi.__global__ import __home_path__, __hyfi_path__
from hyfi.__global__.config import __global_config__
from hyfi.composer import Composer, DictKeyType, SpecialKeys
from hyfi.composer.extended import XC
from hyfi.dotenv import DotEnvConfig
from hyfi.joblib import JobLibConfig
from hyfi.pipe import PIPE, PipeConfig
from hyfi.project import ProjectConfig
from hyfi.utils.datasets import DatasetLikeType, Datasets, DatasetType
from hyfi.utils.envs import Envs
from hyfi.utils.funcs import Funcs
from hyfi.utils.gpumon import nvidia_smi, set_cuda
from hyfi.utils.iolibs import IOLibs
from hyfi.utils.logging import Logging
from hyfi.utils.notebooks import NBs
from hyfi.utils.packages import Packages
from hyfi.utils.types import PathLikeType

logger = Logging.getLogger(__name__)


def _about(cfg):
    pkg_name = cfg.about.__package_name__
    name = cfg.about.name
    print()
    for k, v in cfg.about.dict().items():
        if k.startswith("_"):
            continue
        print(f"{k:11} : {v}")
    if pkg_name:
        print(f"\nExecute `{pkg_name} --help` to see what you can do with {name}")


class HyFI:
    """Primary class for the hyfi config package"""

    config = __global_config__
    SpeicialKeys = SpecialKeys
    __version__ = __global_config__.__version__
    __hyfi_path__ = __hyfi_path__()
    __home_path__ = __home_path__()

    def __init__(self) -> None:
        raise NotImplementedError("Use one of the static construction functions")

    @staticmethod
    def about() -> None:
        """Print the about information"""
        cfg = __global_config__
        _about(cfg)

    @staticmethod
    def init_workspace(
        project_name: str = "",
        task_name: str = "",
        project_description: str = "",
        project_root: str = "",
        project_workspace_name: str = "",
        global_hyfi_root: str = "",
        global_workspace_name: str = "",
        num_workers: int = -1,
        log_level: str = "",
        reinit: bool = True,
        autotime: bool = True,
        retina: bool = True,
        verbose: Union[bool, int] = False,
        **kwargs,
    ) -> ProjectConfig:
        """
        Initialize and start hyfi.

        Args:
                project_name: Name of the project to use.
                task_name: Name of the task to use.
                project_description: Description of the project that will be used.
                project_root: Root directory of the project.
                project_workspace_name: Name of the project's workspace directory.
                global_hyfi_root: Root directory of the global hyfi.
                global_workspace_name: Name of the global hierachical workspace directory.
                num_workers: Number of workers to run.
                log_level: Log level for the log.
                autotime: Whether to automatically set time and / or keep track of run times.
                retina: Whether to use retina or not.
                verbose: Enables or disables logging
        """
        __global_config__.init_workspace(
            project_name=project_name,
            task_name=task_name,
            project_description=project_description,
            project_root=project_root,
            project_workspace_name=project_workspace_name,
            global_hyfi_root=global_hyfi_root,
            global_workspace_name=global_workspace_name,
            num_workers=num_workers,
            log_level=log_level,
            reinit=reinit,
            autotime=autotime,
            retina=retina,
            verbose=verbose,
            **kwargs,
        )
        if __global_config__.project:
            return __global_config__.project
        else:
            raise ValueError("Project not initialized.")

    @staticmethod
    def initialize(config: Union[DictConfig, Dict] = None):  # type: ignore
        """Initialize the global config"""
        __global_config__.initialize(config)

    @staticmethod
    def terminate():
        """Terminate the global config"""
        __global_config__.terminate()

    @staticmethod
    def joblib(**kwargs) -> JobLibConfig:
        """Return the joblib pipe"""
        return JobLibConfig(**kwargs)

    @staticmethod
    def dotenv(**kwargs) -> DotEnvConfig:
        """Return the DotEnvConfig"""
        return DotEnvConfig(**kwargs)

    @staticmethod
    def osenv():
        """Return the DotEnvConfig"""
        return os.environ

    @staticmethod
    def pipe_config(**kwargs) -> PipeConfig:
        """Return the PipeConfig"""
        return PipeConfig(**kwargs)

    @staticmethod
    def compose(
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        return_as_dict: bool = True,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        root_config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        global_package: bool = False,
        verbose: bool = False,
    ) -> Union[DictConfig, Dict]:
        """
        Compose a configuration by applying overrides

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group_name.key=value`)
            return_as_dict: Return the result as a dict
            throw_on_resolution_failure: If True throw an exception if resolution fails
            throw_on_missing: If True throw an exception if config_group doesn't exist
            root_config_name: Name of the root config to be used (e.g. `hconf`)
            config_module: Module of the config to be used (e.g. `hyfi.conf`)
            global_package: If True, the config assumed to be a global package
            verbose: If True print configuration to stdout

        Returns:
            A config object or a dictionary with the composed config
        """
        return Composer._compose(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            return_as_dict=return_as_dict,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            config_name=root_config_name,
            config_module=config_module,
            global_package=global_package,
            verbose=verbose,
        )

    @staticmethod
    def select(
        cfg: Any,
        key: str,
        *,
        default: Any = None,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
    ):
        return Composer.select(
            cfg,
            key,
            default=default,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
        )

    @staticmethod
    def to_dict(
        cfg: Any,
    ):
        return Composer.to_dict(cfg)

    @staticmethod
    def to_config(
        cfg: Any,
    ):
        return Composer.to_config(cfg)

    @staticmethod
    def to_yaml(cfg: Any, resolve: bool = False, sort_keys: bool = False) -> str:
        return Composer.to_yaml(cfg, resolve=resolve, sort_keys=sort_keys)

    @staticmethod
    def to_container(
        cfg: Any,
        *,
        resolve: bool = False,
        throw_on_missing: bool = False,
        enum_to_str: bool = False,
        structured_config_mode: SCMode = SCMode.DICT,
    ):
        return Composer.to_container(
            cfg=cfg,
            resolve=resolve,
            throw_on_missing=throw_on_missing,
            enum_to_str=enum_to_str,
            structured_config_mode=structured_config_mode,
        )

    @staticmethod
    def partial(
        config: Union[str, Dict],
        *args: Any,
        **kwargs: Any,
    ) -> Callable:
        return XC.partial(config, *args, **kwargs)

    @staticmethod
    def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
        return XC.instantiate(config, *args, **kwargs)

    @staticmethod
    def is_config(
        cfg: Any,
    ):
        return Composer.is_config(cfg)

    @staticmethod
    def is_list(
        cfg: Any,
    ):
        return Composer.is_list(cfg)

    @staticmethod
    def is_instantiatable(cfg: Any):
        return Composer.is_instantiatable(cfg)

    @staticmethod
    def load(file_: Union[str, Path, IO[Any]]) -> Union[DictConfig, ListConfig]:
        return Composer.load(file_)

    @staticmethod
    def update(_dict, _overrides):
        return Composer.update(_dict, _overrides)

    @staticmethod
    def merge(
        *configs: Union[
            DictConfig,
            ListConfig,
            Dict[DictKeyType, Any],
            List[Any],
            Tuple[Any, ...],
            Any,
        ],
    ) -> Union[ListConfig, DictConfig]:
        """
        Merge a list of previously created configs into a single one
        :param configs: Input configs
        :return: the merged config object.
        """
        return Composer.merge(*configs)

    @staticmethod
    def save(config: Any, f: Union[str, Path, IO[Any]], resolve: bool = False) -> None:
        Composer.save(config, f, resolve)

    @staticmethod
    def save_json(
        json_dict: dict,
        f: Union[str, Path, IO[Any]],
        indent=4,
        ensure_ascii=False,
        default=None,
        **kwargs,
    ):
        Composer.save_json(json_dict, f, indent, ensure_ascii, default, **kwargs)

    @staticmethod
    def load_json(f: Union[str, Path, IO[Any]], **kwargs) -> dict:
        return Composer.load_json(f, **kwargs)

    @staticmethod
    def pprint(cfg: Any, resolve: bool = True, **kwargs):
        Composer.print(cfg, resolve=resolve, **kwargs)

    @staticmethod
    def print(cfg: Any, resolve: bool = True, **kwargs):
        Composer.print(cfg, resolve=resolve, **kwargs)

    @staticmethod
    def methods(cfg: Any, obj: object, return_function=False):
        return Composer.methods(cfg, obj, return_function)

    @staticmethod
    def function(cfg: Any, _name_, return_function=False, **parms):
        return XC.function(cfg, _name_, return_function, **parms)

    @staticmethod
    def run(config: Any, **kwargs: Any) -> Any:
        XC.run(config, **kwargs)

    @staticmethod
    def ensure_list(value):
        return Composer.ensure_list(value)

    @staticmethod
    def ensure_kwargs(_kwargs, _fn):
        return Composer.ensure_kwargs(_kwargs, _fn)

    @staticmethod
    def getsource(obj):
        return XC.getsource(obj)

    @staticmethod
    def viewsource(obj):
        return XC.viewsource(obj)

    ###############################
    # Logging related functions
    ###############################
    @staticmethod
    def getLogger(
        name=None,
        log_level=None,
    ):
        return Logging.getLogger(name, log_level)

    @staticmethod
    def setLogger(level=None, force=True, **kwargs):
        return Logging.setLogger(level, force, **kwargs)

    ###############################
    # Batcher related functions
    ###############################
    @staticmethod
    def pipe(data: Any, pipe_config: Union[Dict, PipeConfig]):
        return PIPE.pipe(data, pipe_config)

    @staticmethod
    def apply(
        func: Callable,
        series: Union[pd.Series, pd.DataFrame, Sequence, Mapping],
        description: Optional[str] = None,
        use_batcher: bool = True,
        minibatch_size: Optional[int] = None,
        num_workers: Optional[int] = None,
        **kwargs,
    ):
        return PIPE.apply(
            func,
            series,
            description=description,
            use_batcher=use_batcher,
            minibatch_size=minibatch_size,
            num_workers=num_workers,
            **kwargs,
        )

    ###############################
    # Dataset related functions
    ###############################
    @staticmethod
    def load_dataset(
        path: str,
        name: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[
            Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]
        ] = None,
        split: Optional[str] = None,
        cache_dir: Optional[str] = None,
        ignore_verifications="deprecated",
        keep_in_memory: Optional[bool] = None,
        save_infos: bool = False,
        use_auth_token: Optional[Union[bool, str]] = None,
        streaming: bool = False,
        num_proc: Optional[int] = None,
        storage_options: Optional[Dict] = None,
        **config_kwargs,
    ) -> DatasetLikeType:
        """Load a dataset from the Hugging Face Hub, or a local dataset.

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
        return Datasets.load_dataset(
            path=path,
            name=name,
            data_dir=data_dir,
            data_files=data_files,
            split=split,
            cache_dir=cache_dir,
            ignore_verifications=ignore_verifications,
            keep_in_memory=keep_in_memory,
            save_infos=save_infos,
            use_auth_token=use_auth_token,
            streaming=streaming,
            num_proc=num_proc,
            storage_options=storage_options,
            **config_kwargs,
        )

    @staticmethod
    def dict_to_dataframe(
        data,
        orient="columns",
        dtype=None,
        columns=None,
    ):
        return Datasets.dict_to_dataframe(data, orient, dtype, columns)

    @staticmethod
    def records_to_dataframe(
        data,
        index=None,
        exclude=None,
        columns=None,
        coerce_float=False,
        nrows=None,
    ):
        return Datasets.records_to_dataframe(
            data, index, exclude, columns, coerce_float, nrows
        )

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
    ):
        return Datasets.concatenate_data(
            data,
            columns,
            add_split_key_column,
            added_column_name,
            ignore_index,
            axis,
            split,
            verbose,
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
        return Datasets.concatenate_dataframes(
            data,
            columns,
            add_split_key_column,
            added_column_name,
            ignore_index,
            axis,
            verbose,
            **kwargs,
        )

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
        return Datasets.load_data(
            path,
            name,
            data_dir,
            data_files,
            split,
            filetype,
            concatenate,
            use_cached,
            verbose,
            **kwargs,
        )

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
        return Datasets.get_data_files(
            data_files, data_dir, split, recursive, use_cached, verbose, **kwargs
        )

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
        return Datasets.load_dataframes(
            data_files,
            data_dir,
            filetype,
            split,
            concatenate,
            ignore_index,
            use_cached,
            verbose,
            **kwargs,
        )

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
        return Datasets.load_dataframe(
            data_file, data_dir, filetype, columns, index_col, verbose, **kwargs
        )

    @staticmethod
    def save_dataframe(
        data: pd.DataFrame,
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
        Datasets.save_dataframes(
            data,
            data_file,
            data_dir,
            columns,
            index,
            filetype,
            suffix,
            verbose,
            **kwargs,
        )

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
        Datasets.save_dataframes(
            data,
            data_file,
            data_dir,
            columns,
            index,
            filetype,
            suffix,
            verbose,
            **kwargs,
        )

    @staticmethod
    def is_dataframe(data) -> bool:
        return Datasets.is_dataframe(data)

    @staticmethod
    def to_datetime(data, _format=None, _columns=None, **kwargs):
        return Datasets.to_datetime(data, _format, _columns, **kwargs)

    @staticmethod
    def to_numeric(data, _columns=None, errors="coerce", downcast=None, **kwargs):
        return Datasets.to_numeric(data, _columns, errors, downcast, **kwargs)

    ###############################
    # Notebook functions
    ###############################
    @staticmethod
    def is_colab():
        return NBs.is_colab()

    @staticmethod
    def is_notebook():
        return NBs.is_notebook()

    @staticmethod
    def mount_google_drive(
        project_root: str = "",
        project_name: str = "",
        mountpoint: str = "/content/drive",
        force_remount: bool = False,
        timeout_ms: int = 120000,
    ):
        return NBs.mount_google_drive(
            project_root, project_name, mountpoint, force_remount, timeout_ms
        )

    @staticmethod
    def clear_output(wait=False):
        return NBs.clear_output(wait)

    @staticmethod
    def display(
        *objs,
        include=None,
        exclude=None,
        metadata=None,
        transient=None,
        display_id=None,
        **kwargs,
    ):
        return NBs.display(
            *objs,
            include=include,
            exclude=exclude,
            metadata=metadata,
            transient=transient,
            display_id=display_id,
            **kwargs,
        )

    @staticmethod
    def display_image(
        data=None,
        url=None,
        filename=None,
        format=None,
        embed=None,
        width=None,
        height=None,
        retina=False,
        unconfined=False,
        metadata=None,
        **kwargs,
    ):
        return NBs.display_image(
            data=data,
            url=url,
            filename=filename,
            format=format,
            embed=embed,
            width=width,
            height=height,
            retina=retina,
            unconfined=unconfined,
            metadata=metadata,
            **kwargs,
        )

    @staticmethod
    def get_display():
        return NBs.get_display()

    @staticmethod
    def hide_code_in_slideshow():
        return NBs.hide_code_in_slideshow()

    @staticmethod
    def cprint(str_color_tuples, **kwargs):
        return NBs.cprint(str_color_tuples)

    @staticmethod
    def create_dropdown(
        options,
        value,
        description,
        disabled=False,
        style=None,
        layout=None,
        **kwargs,
    ):
        if style is None:
            style = {"description_width": "initial"}
        return NBs.create_dropdown(
            options,
            value,
            description,
            disabled,
            style,
            layout,
            **kwargs,
        )

    @staticmethod
    def create_textarea(
        value,
        description,
        placeholder="",
        disabled=False,
        style=None,
        layout=None,
        **kwargs,
    ):
        if style is None:
            style = {"description_width": "initial"}
        return NBs.create_textarea(
            value,
            description,
            placeholder,
            disabled,
            style,
            layout,
            **kwargs,
        )

    @staticmethod
    def create_button(
        description,
        button_style="",
        icon="check",
        layout=None,
        **kwargs,
    ):
        return NBs.create_button(description, button_style, icon, layout, **kwargs)

    @staticmethod
    def create_radiobutton(
        options,
        description,
        value=None,
        disabled=False,
        style=None,
        layout=None,
        **kwargs,
    ):
        if style is None:
            style = {"description_width": "initial"}
        return NBs.create_radiobutton(
            options,
            description,
            value,
            disabled,
            style,
            layout,
            **kwargs,
        )

    @staticmethod
    def create_image(
        filename=None,
        format=None,
        width=None,
        height=None,
        **kwargs,
    ):
        return NBs.create_image(filename, format, width, height, **kwargs)

    @staticmethod
    def create_floatslider(
        min=0.0,
        max=1.0,
        step=0.1,
        value=None,
        description="",
        disabled=False,
        continuous_update=False,
        orientation="horizontal",
        readout=True,
        readout_format=".1f",
        style=None,
        layout=None,
        **kwargs,
    ):
        if style is None:
            style = {"description_width": "initial"}
        return NBs.create_floatslider(
            min,
            max,
            step,
            value,
            description,
            disabled,
            continuous_update,
            orientation,
            readout,
            readout_format,
            style,
            layout,
            **kwargs,
        )

    ###############################
    # Envs functions
    ###############################
    @staticmethod
    def expand_posix_vars(posix_expr: str, context: dict = None) -> str:  # type: ignore
        """
        Expand POSIX variables in a string.

        Args:
            posix_expr (str): The string containing POSIX variables to be expanded.
            context (dict, optional): A dictionary containing additional variables to be used in the expansion.
                Defaults to None.

        Returns:
            str: The expanded string.

        Examples:
            >>> expand_posix_vars("$HOME")
            '/home/user'
            >>> expand_posix_vars("$HOME/$USER", {"USER": "testuser"})
            '/home/user/testuser'

        """
        return Envs.expand_posix_vars(posix_expr, context=context)

    @staticmethod
    def get_osenv(key: str = "", default: Union[str, None] = None) -> Any:
        """Get the value of an environment variable or return the default value"""
        return Envs.get_osenv(key, default=default)

    @staticmethod
    def set_osenv(key, value):
        return Envs.set_osenv(key, value)

    @staticmethod
    def load_dotenv(
        override: bool = False,
        dotenv_dir: str = "",
        dotenv_filename: str = ".env",
        verbose: bool = False,
    ) -> None:
        Envs.load_dotenv(
            override=override,
            dotenv_filename=dotenv_filename,
            dotenv_dir=dotenv_dir,
            verbose=verbose,
        )

    ###############################
    # Packages functions
    ###############################
    @staticmethod
    def ensure_import_module(
        name: str,
        libpath: str,
        liburi: str,
        specname: str = "",
        syspath: str = "",
    ):
        return Packages.ensure_import_module(name, libpath, liburi, specname, syspath)

    @staticmethod
    def pip(
        name: str,
        upgrade: bool = False,
        prelease: bool = False,
        editable: bool = False,
        quiet: bool = True,
        find_links: str = "",
        requirement: bool = False,
        force_reinstall: bool = False,
        verbose: bool = False,
        **kwargs,
    ):
        return Packages.pip(
            name,
            upgrade,
            prelease,
            editable,
            quiet,
            find_links,
            requirement,
            force_reinstall,
            verbose,
            **kwargs,
        )

    @staticmethod
    def pipu(
        prelease=False,
        quiet=False,
        force_reinstall=False,
        **kwargs,
    ):
        return Packages.pip(
            name="hyfi",
            upgrade=True,
            prelease=prelease,
            quiet=quiet,
            force_reinstall=force_reinstall,
            **kwargs,
        )

    ###############################
    # Files functions
    ###############################
    @staticmethod
    def exists(a, *p):
        return IOLibs.exists(a, *p)

    @staticmethod
    def is_file(a, *p):
        return IOLibs.is_file(a, *p)

    @staticmethod
    def is_dir(a, *p):
        return IOLibs.is_dir(a, *p)

    @staticmethod
    def mkdir(_path: str):
        return IOLibs.mkdir(_path)

    @staticmethod
    def join_path(a, *p):
        return IOLibs.join_path(a, *p)

    @staticmethod
    def get_filepaths(
        filename_patterns: Union[str, PosixPath, WindowsPath],
        base_dir: Union[str, PosixPath, WindowsPath] = "",
        recursive: bool = True,
        verbose: bool = False,
        **kwargs,
    ):
        return IOLibs.get_filepaths(
            filename_patterns,
            base_dir=base_dir,
            recursive=recursive,
            verbose=verbose,
            **kwargs,
        )

    @staticmethod
    def read(uri, mode="rb", encoding=None, head=None, **kwargs):
        return IOLibs.read(uri, mode, encoding, head, **kwargs)

    @staticmethod
    def copy(
        src: PathLikeType,
        dst: PathLikeType,
        follow_symlinks: bool = True,
    ):
        """
        Copy a file or directory. This is a wrapper around shutil.copy.
        If you need to copy an entire directory (including all of its contents), or if you need to overwrite existing files in the destination directory, shutil.copy() would be a better choice.

        Args:
                src: Path to the file or directory to be copied.
                dst: Path to the destination directory. If the destination directory does not exist it will be created.
                follow_symlinks: Whether or not symlinks should be followed
        """
        IOLibs.copy(src, dst, follow_symlinks=follow_symlinks)

    @staticmethod
    def copyfile(
        src: PathLikeType,
        dst: PathLikeType,
        follow_symlinks: bool = True,
    ):
        """
        Copy a file or directory. This is a wrapper around shutil.copyfile.
        If you want to copy a single file from one location to another, shutil.copyfile() is the appropriate function to use.

        Args:
                src: Path to the file or directory to copy.
                dst: Path to the destination file or directory. If the destination file already exists it will be overwritten.
                follow_symlinks: Whether to follow symbolic links or not
        """
        IOLibs.copyfile(src, dst, follow_symlinks=follow_symlinks)

    @staticmethod
    def cached_path(
        url_or_filename: str,
        extract_archive: bool = False,
        force_extract: bool = False,
        return_parent_dir: bool = False,
        cache_dir: str = "",
        verbose: bool = False,
    ):
        """
        Attempts to cache a file or URL and return the path to the cached file.
        If required libraries 'cached_path' and 'gdown' are not installed, raises an ImportError.

        Args:
            url_or_filename (str): The URL or filename to be cached.
            extract_archive (bool, optional): Whether to extract the file if it's an archive. Defaults to False.
            force_extract (bool, optional): Whether to force extraction even if the destination already exists. Defaults to False.
            return_parent_dir (bool, optional): If True, returns the parent directory of the cached file. Defaults to False.
            cache_dir (str, optional): Directory to store cached files. Defaults to None.
            verbose (bool, optional): Whether to print informative messages during the process. Defaults to False.

        Raises:
            ImportError: If the required libraries 'cached_path' and 'gdown' are not imported.

        Returns:
            str: Path to the cached file or its parent directory, depending on the 'return_parent_dir' parameter.
        """
        return IOLibs.cached_path(
            url_or_filename,
            extract_archive=extract_archive,
            force_extract=force_extract,
            return_parent_dir=return_parent_dir,
            cache_dir=cache_dir,
            verbose=verbose,
        )

    ###############################
    # Utility functions
    ###############################
    @staticmethod
    def to_dateparm(_date, _format="%Y-%m-%d"):
        return Funcs.to_dateparm(_date, _format)

    @staticmethod
    def dict_product(dicts):
        return Funcs.dict_product(dicts)

    ###############################
    # GPU Utility functions
    ###############################
    @staticmethod
    def nvidia_smi():
        return nvidia_smi()

    @staticmethod
    def set_cuda(device=0):
        return set_cuda(device)

    @staticmethod
    def gpu_usage(all=False, attrList=None, useOldCode=False):
        """
        Show GPU utilization in human readable format. This is a wrapper around the GPUtil library.

        Args:
                all: If True show all available GPUs ( default : False )
                attrList: List of attributes to show ( default : None )
                useOldCode: If True use old code instead of new code ( default : False )

        Returns:
                A string with the
        """
        try:
            from GPUtil import showUtilization  # type: ignore
        except ImportError:
            logger.error("GPUtil is not installed. To install, run: pip install GPUtil")
            return

        return showUtilization(all, attrList, useOldCode)

    ###############################
    # Graphics functions
    ###############################
    @staticmethod
    def collage(
        images_or_uris,
        collage_filepath=None,
        ncols=3,
        max_images=12,
        collage_width=1200,
        padding: int = 10,
        bg_color: str = "black",
        crop_to_min_size=False,
        show_filename=False,
        filename_offset=(5, 5),
        fontname=None,
        fontsize=12,
        fontcolor="#000",
        **kwargs,
    ):
        from hyfi.graphics.collage import collage as _collage

        return _collage(
            images_or_uris,
            collage_filepath=collage_filepath,
            ncols=ncols,
            max_images=max_images,
            collage_width=collage_width,
            padding=padding,
            bg_color=bg_color,
            crop_to_min_size=crop_to_min_size,
            show_filename=show_filename,
            filename_offset=filename_offset,
            fontname=fontname,
            fontsize=fontsize,
            fontcolor=fontcolor,
            **kwargs,
        )

    @staticmethod
    def make_gif(
        image_filepaths=None,
        filename_patterns: str = "",
        base_dir: str = "",
        output_filepath: str = "",
        duration: int = 100,
        loop: int = 0,
        width: int = 0,
        optimize: bool = True,
        quality: int = 50,
        show: bool = False,
        force: bool = False,
        **kwargs,
    ):
        from hyfi.graphics.motion import make_gif as _make_gif

        return _make_gif(
            image_filepaths=image_filepaths,
            filename_patterns=filename_patterns,
            base_dir=base_dir,
            output_filepath=output_filepath,
            duration=duration,
            loop=loop,
            width=width,
            optimize=optimize,
            quality=quality,
            show=show,
            force=force,
            **kwargs,
        )

    @staticmethod
    def get_image_font(fontname: str = "", fontsize: int = 12):
        from hyfi.graphics.utils import get_image_font

        return get_image_font(fontname, fontsize)

    @staticmethod
    def load_image(
        image_or_uri,
        max_width: int = 0,
        max_height: int = 0,
        max_pixels: int = 0,
        scale: float = 1.0,
        resize_to_multiple_of: int = 0,
        crop_box=None,
        mode="RGB",
        **kwargs,
    ):
        from hyfi.graphics.utils import load_image

        return load_image(
            image_or_uri,
            max_width,
            max_height,
            max_pixels,
            scale,
            resize_to_multiple_of,
            crop_box,
            mode,
            **kwargs,
        )

    @staticmethod
    def scale_image(
        image,
        max_width: int = 0,
        max_height: int = 0,
        max_pixels: int = 0,
        scale: float = 1.0,
        resize_to_multiple_of: int = 8,
        resample: int = 1,
    ):
        """
        Scale an image to a maximum width, height, or number of pixels.

        resample:   Image.NEAREST (0), Image.LANCZOS (1), Image.BILINEAR (2),
                    Image.BICUBIC (3), Image.BOX (4) or Image.HAMMING (5)
        """
        from hyfi.graphics.utils import scale_image

        return scale_image(
            image,
            max_width,
            max_height,
            max_pixels,
            scale,
            resize_to_multiple_of,
            resample,
        )

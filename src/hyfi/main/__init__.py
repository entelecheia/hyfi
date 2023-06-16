"""
    This module contains the primary class for the hyfi config package, HyFI,
    as well as various utility functions and imports.
"""
from pathlib import Path
from typing import IO, Any, Dict, List, Tuple, Union

from omegaconf import DictConfig, ListConfig, SCMode

from hyfi.__global__ import __home_path__, __hyfi_path__
from hyfi.__global__.config import __global_config__
from hyfi.cached_path import cached_path
from hyfi.dotenv import DotEnvConfig
from hyfi.hydra import _compose, _select, _to_config, _to_dict
from hyfi.hydra.main import (
    DictKeyType,
    SpecialKeys,
    _ensure_kwargs,
    _ensure_list,
    _function,
    _getsource,
    _instantiate,
    _is_config,
    _is_instantiatable,
    _is_list,
    _load,
    _load_json,
    _merge,
    _methods,
    _partial,
    _print,
    _run,
    _save,
    _save_json,
    _to_container,
    _to_yaml,
    _update,
    _viewsource,
)
from hyfi.joblib.pipe import _apply, _pipe
from hyfi.project import ProjectConfig
from hyfi.utils.env import expand_posix_vars, get_osenv, load_dotenv, set_osenv
from hyfi.utils.file import exists, is_dir, is_file, join_path, mkdir
from hyfi.utils.func import (
    dict_product,
    dict_to_dataframe,
    records_to_dataframe,
    to_dateparm,
    to_datetime,
    to_numeric,
)
from hyfi.utils.google import mount_google_drive
from hyfi.utils.gpu import nvidia_smi, set_cuda
from hyfi.utils.logging import getLogger, setLogger
from hyfi.utils.notebook import (
    clear_output,
    cprint,
    create_button,
    create_dropdown,
    create_floatslider,
    create_image,
    create_radiobutton,
    create_textarea,
    display,
    display_image,
    get_display,
    hide_code_in_slideshow,
    is_colab,
    is_notebook,
)

logger = getLogger(__name__)


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
    def initialize(config: Union[DictConfig, Dict] = None):  # type: ignore
        """Initialize the global config"""
        __global_config__.initialize(config)

    @staticmethod
    def terminate():
        """Terminate the global config"""
        __global_config__.terminate()

    @staticmethod
    def envs() -> DotEnvConfig:
        """Return the current environments"""
        return DotEnvConfig()  # type: ignore

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
        return expand_posix_vars(posix_expr, context=context)

    @staticmethod
    def environ(key: str = "", default: Union[str, None] = None) -> Any:
        """Get the value of an environment variable or return the default value"""
        return get_osenv(key, default=default)

    @staticmethod
    def compose(
        config_group: Union[str, None] = None,
        overrides: Union[List[str], None] = None,
        config_data: Union[Dict[str, Any], DictConfig, None] = None,
        *,
        return_as_dict: bool = True,
        throw_on_resolution_failure: bool = True,
        throw_on_missing: bool = False,
        config_name: Union[str, None] = None,
        config_module: Union[str, None] = None,
        global_package: bool = False,
        verbose: bool = False,
    ) -> Union[DictConfig, Dict]:
        """
        Compose a configuration by applying overrides

        Args:
            config_group: Name of the config group to compose (`config_group=name`)
            overrides: List of config groups to apply overrides to (`overrides=["override_name"]`)
            config_data: Keyword arguments to override config group values (will be converted to overrides of the form `config_group.key=value`)
            return_as_dict: Return the result as a dict
            throw_on_resolution_failure: If True throw an exception if resolution fails
            throw_on_missing: If True throw an exception if config_group doesn't exist
            config_name: Name of the root config to be used (e.g. `hconf`)
            config_module: Module of the config to be used (e.g. `hyfi.conf`)
            global_package: If True, the config assumed to be a global package
            verbose: If True print configuration to stdout

        Returns:
            A config object or a dictionary with the composed config
        """
        return _compose(
            config_group=config_group,
            overrides=overrides,
            config_data=config_data,
            return_as_dict=return_as_dict,
            throw_on_resolution_failure=throw_on_resolution_failure,
            throw_on_missing=throw_on_missing,
            config_name=config_name,
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
        return _select(
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
        return _to_dict(cfg)

    @staticmethod
    def to_config(
        cfg: Any,
    ):
        return _to_config(cfg)

    @staticmethod
    def to_yaml(cfg: Any, *, resolve: bool = False, sort_keys: bool = False) -> str:
        if resolve:
            cfg = _to_dict(cfg)
        return _to_yaml(cfg, resolve=resolve, sort_keys=sort_keys)

    @staticmethod
    def to_container(
        cfg: Any,
        *,
        resolve: bool = False,
        throw_on_missing: bool = False,
        enum_to_str: bool = False,
        structured_config_mode: SCMode = SCMode.DICT,
    ):
        return _to_container(
            cfg=cfg,
            resolve=resolve,
            throw_on_missing=throw_on_missing,
            enum_to_str=enum_to_str,
            structured_config_mode=structured_config_mode,
        )

    @staticmethod
    def partial(
        config: Any = None,
        config_group: Union[str, None] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return _partial(config=config, config_group=config_group, *args, **kwargs)

    @staticmethod
    def instantiate(config: Any, *args: Any, **kwargs: Any) -> Any:
        return _instantiate(config, *args, **kwargs)

    @staticmethod
    def is_config(
        cfg: Any,
    ):
        return _is_config(cfg)

    @staticmethod
    def is_list(
        cfg: Any,
    ):
        return _is_list(cfg)

    @staticmethod
    def is_instantiatable(cfg: Any):
        return _is_instantiatable(cfg)

    @staticmethod
    def load(file_: Union[str, Path, IO[Any]]) -> Union[DictConfig, ListConfig]:
        return _load(file_)

    @staticmethod
    def update(_dict, _overrides):
        return _update(_dict, _overrides)

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
        return _merge(*configs)

    @staticmethod
    def save(config: Any, f: Union[str, Path, IO[Any]], resolve: bool = False) -> None:
        _save(config, f, resolve)

    @staticmethod
    def save_json(
        json_dict: dict,
        f: Union[str, Path, IO[Any]],
        indent=4,
        ensure_ascii=False,
        default=None,
        **kwargs,
    ):
        _save_json(json_dict, f, indent, ensure_ascii, default, **kwargs)

    @staticmethod
    def load_json(f: Union[str, Path, IO[Any]], **kwargs) -> dict:
        return _load_json(f, **kwargs)

    @staticmethod
    def pprint(cfg: Any, resolve: bool = True, **kwargs):
        _print(cfg, resolve=resolve, **kwargs)

    @staticmethod
    def print(cfg: Any, resolve: bool = True, **kwargs):
        _print(cfg, resolve=resolve, **kwargs)

    @staticmethod
    def methods(cfg: Any, obj: object, return_function=False):
        return _methods(cfg, obj, return_function)

    @staticmethod
    def function(cfg: Any, _name_, return_function=False, **parms):
        return _function(cfg, _name_, return_function, **parms)

    @staticmethod
    def run(config: Any, **kwargs: Any) -> Any:
        _run(config, **kwargs)

    @staticmethod
    def load_dotenv(
        override: bool = False,
        dotenv_dir: str = "",
        dotenv_filename: str = ".env",
        verbose: bool = False,
    ) -> None:
        load_dotenv(
            override=override,
            dotenv_filename=dotenv_filename,
            dotenv_dir=dotenv_dir,
            verbose=verbose,
        )

    @staticmethod
    def cached_path(
        url_or_filename,
        extract_archive: bool = False,
        force_extract: bool = False,
        return_parent_dir: bool = False,
        cache_dir=None,
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
        return cached_path(
            url_or_filename,
            extract_archive=extract_archive,
            force_extract=force_extract,
            return_parent_dir=return_parent_dir,
            cache_dir=cache_dir,
            verbose=verbose,
        )

    @staticmethod
    def pipe(data=None, cfg=None):
        return _pipe(data, cfg)

    @staticmethod
    def ensure_list(value):
        return _ensure_list(value)

    @staticmethod
    def to_dateparm(_date, _format="%Y-%m-%d"):
        return to_dateparm(_date, _format)

    @staticmethod
    def exists(a, *p):
        return exists(a, *p)

    @staticmethod
    def is_file(a, *p):
        return is_file(a, *p)

    @staticmethod
    def is_dir(a, *p):
        return is_dir(a, *p)

    @staticmethod
    def mkdir(_path: str):
        return mkdir(_path)

    @staticmethod
    def join_path(a, *p):
        return join_path(a, *p)

    @staticmethod
    def apply(
        func,
        series,
        description=None,
        use_batcher=True,
        minibatch_size=None,
        num_workers=None,
        verbose=False,
        **kwargs,
    ):
        return _apply(
            func,
            series,
            description=description,
            use_batcher=use_batcher,
            minibatch_size=minibatch_size,
            num_workers=num_workers,
            verbose=verbose,
            **kwargs,
        )

    @staticmethod
    def ensure_kwargs(_kwargs, _fn):
        return _ensure_kwargs(_kwargs, _fn)

    @staticmethod
    def save_data(
        data,
        filename=None,
        base_dir=None,
        columns=None,
        index=False,
        filetype="parquet",
        suffix=None,
        verbose=False,
        **kwargs,
    ):
        from hyfi.utils.file import save_data

        if filename is None:
            raise ValueError("filename must be specified")
        save_data(
            data,
            filename,
            base_dir=base_dir,
            columns=columns,
            index=index,
            filetype=filetype,
            suffix=suffix,
            verbose=verbose,
            **kwargs,
        )

    @staticmethod
    def load_data(filename=None, base_dir=None, filetype=None, verbose=False, **kwargs):
        from hyfi.utils.file import load_data

        if filename is not None:
            filename = str(filename)
        if SpecialKeys.TARGET in kwargs:
            return _instantiate(
                kwargs,
                filename=filename,
                base_dir=base_dir,
                verbose=verbose,
                filetype=filetype,
            )
        if filename is None:
            raise ValueError("filename must be specified")
        return load_data(
            filename,
            base_dir=base_dir,
            verbose=verbose,
            filetype=filetype,
            **kwargs,
        )

    @staticmethod
    def get_filepaths(
        filename_patterns=None, base_dir=None, recursive=True, verbose=True, **kwargs
    ):
        from hyfi.utils.file import get_filepaths

        if filename_patterns is None:
            raise ValueError("filename must be specified")
        return get_filepaths(
            filename_patterns,
            base_dir=base_dir,
            recursive=recursive,
            verbose=verbose,
            **kwargs,
        )

    @staticmethod
    def concat_data(
        data,
        columns=None,
        add_key_as_name=False,
        name_column="_name_",
        ignore_index=True,
        verbose=False,
        **kwargs,
    ):
        from hyfi.utils.file import concat_data

        return concat_data(
            data,
            columns=columns,
            add_key_as_name=add_key_as_name,
            name_column=name_column,
            ignore_index=ignore_index,
            verbose=verbose,
            **kwargs,
        )

    @staticmethod
    def is_dataframe(data):
        from hyfi.utils.file import is_dataframe

        return is_dataframe(data)

    @staticmethod
    def is_colab():
        return is_colab()

    @staticmethod
    def is_notebook():
        return is_notebook()

    @staticmethod
    def osenv(key, default=None):
        return get_osenv(key, default)

    @staticmethod
    def env_set(key, value):
        return set_osenv(key, value)

    @staticmethod
    def nvidia_smi():
        return nvidia_smi()

    @staticmethod
    def ensure_import_module(name, libpath, liburi, specname=None, syspath=None):
        from hyfi.utils.lib import ensure_import_module

        return ensure_import_module(name, libpath, liburi, specname, syspath)

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
        from hyfi.image.collage import collage as _collage

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
        filename_patterns=None,
        base_dir=None,
        output_filepath=None,
        duration=100,
        loop=0,
        width=None,
        optimize=True,
        quality=50,
        show=False,
        force=False,
        **kwargs,
    ):
        from hyfi.image.motion import make_gif as _make_gif

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
    def to_datetime(data, _format=None, _columns=None, **kwargs):
        return to_datetime(data, _format, _columns, **kwargs)

    @staticmethod
    def to_numeric(data, _columns=None, errors="coerce", downcast=None, **kwargs):
        return to_numeric(data, _columns, errors, downcast, **kwargs)

    @staticmethod
    def getLogger(
        name=None,
        log_level=None,
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ):
        return getLogger(name, log_level, fmt)

    @staticmethod
    def setLogger(level=None, force=True, **kwargs):
        return setLogger(level, force, **kwargs)

    @staticmethod
    def set_cuda(device=0):
        return set_cuda(device)

    @staticmethod
    def mount_google_drive(
        project_root: str = "",
        project_name: str = "",
        mountpoint: str = "/content/drive",
        force_remount: bool = False,
        timeout_ms: int = 120000,
    ):
        return mount_google_drive(
            project_root, project_name, mountpoint, force_remount, timeout_ms
        )

    @staticmethod
    def getsource(obj):
        return _getsource(obj)

    @staticmethod
    def viewsource(obj):
        return _viewsource(obj)

    @staticmethod
    def clear_output(wait=False):
        return clear_output(wait)

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
        return display(
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
        return display_image(
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
    def pip(
        name,
        upgrade=False,
        prelease=False,
        editable=False,
        quiet=False,
        find_links=None,
        requirement=None,
        force_reinstall=False,
        verbose=False,
        **kwargs,
    ):
        from hyfi.utils.lib import pip as _pip

        return _pip(
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
    def upgrade(prelease=False, quiet=False, force_reinstall=False, **kwargs):
        from hyfi.utils.lib import pip

        return pip(
            name="hyfi",
            upgrade=True,
            prelease=prelease,
            quiet=quiet,
            force_reinstall=force_reinstall,
            **kwargs,
        )

    @staticmethod
    def dict_product(dicts):
        return dict_product(dicts)

    @staticmethod
    def get_display():
        return get_display()

    @staticmethod
    def hide_code_in_slideshow():
        return hide_code_in_slideshow()

    @staticmethod
    def cprint(str_color_tuples, **kwargs):
        return cprint(str_color_tuples)

    @staticmethod
    def dict_to_dataframe(data, orient="columns", dtype=None, columns=None):
        return dict_to_dataframe(data, orient, dtype, columns)

    @staticmethod
    def records_to_dataframe(
        data, index=None, exclude=None, columns=None, coerce_float=False, nrows=None
    ):
        return records_to_dataframe(data, index, exclude, columns, coerce_float, nrows)

    @staticmethod
    def create_dropdown(
        options, value, description, disabled=False, style=None, layout=None, **kwargs
    ):
        if style is None:
            style = {"description_width": "initial"}
        return create_dropdown(
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
        return create_textarea(
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
        description, button_style="", icon="check", layout=None, **kwargs
    ):
        return create_button(description, button_style, icon, layout, **kwargs)

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
        return create_radiobutton(
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
        return create_image(filename, format, width, height, **kwargs)

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
        return create_floatslider(
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

    @staticmethod
    def get_image_font(fontname=None, fontsize=12):
        from hyfi.image.collage import get_image_font

        return get_image_font(fontname, fontsize)

    @staticmethod
    def read(uri, mode="rb", encoding=None, head=None, **kwargs):
        from hyfi.utils.file import read as _read

        return _read(uri, mode, encoding, head, **kwargs)

    @staticmethod
    def load_image(
        image_or_uri,
        max_width: int = None,
        max_height: int = None,
        max_pixels: int = None,
        scale: float = 1.0,
        resize_to_multiple_of: int = None,
        crop_box=None,
        mode="RGB",
        **kwargs,
    ):
        from hyfi.image.utils import load_image as _load_image

        return _load_image(
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
    def scale_image(
        image,
        max_width: int = None,
        max_height: int = None,
        max_pixels: int = None,
        scale: float = 1.0,
        resize_to_multiple_of: int = 8,
        resample: int = 1,
    ):
        """
        Scale an image to a maximum width, height, or number of pixels.

        resample:   Image.NEAREST (0), Image.LANCZOS (1), Image.BILINEAR (2),
                    Image.BICUBIC (3), Image.BOX (4) or Image.HAMMING (5)
        """
        from hyfi.image.utils import scale_image as _scale_image

        return _scale_image(
            image,
            max_width,
            max_height,
            max_pixels,
            scale,
            resize_to_multiple_of,
            resample,
        )

    @staticmethod
    def copy(src, dst, *, follow_symlinks=True):
        """
        Copy a file or directory. This is a wrapper around shutil.copy.
        If you need to copy an entire directory (including all of its contents), or if you need to overwrite existing files in the destination directory, shutil.copy() would be a better choice.

        Args:
                src: Path to the file or directory to be copied.
                dst: Path to the destination directory. If the destination directory does not exist it will be created.
                follow_symlinks: Whether or not symlinks should be followed
        """
        import shutil

        src = str(src)
        dst = str(dst)
        mkdir(dst)
        shutil.copy(src, dst, follow_symlinks=follow_symlinks)
        logger.info(f"copied {src} to {dst}")

    @staticmethod
    def copyfile(src, dst, *, follow_symlinks=True):
        """
        Copy a file or directory. This is a wrapper around shutil.copyfile.
        If you want to copy a single file from one location to another, shutil.copyfile() is the appropriate function to use.

        Args:
                src: Path to the file or directory to copy.
                dst: Path to the destination file or directory. If the destination file already exists it will be overwritten.
                follow_symlinks: Whether to follow symbolic links or not
        """
        import shutil

        src = str(src)
        dst = str(dst)
        shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)
        logger.info(f"copied {src} to {dst}")

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

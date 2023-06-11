"""Environment variable utilities"""
import os
from pathlib import Path
from typing import Any
from string import Template
from collections import defaultdict

import dotenv
import hydra

from ..io.file import is_dir
from .logging import getLogger

logger = getLogger(__name__)


def getcwd():
    """Get the original working directory before Hydra changed it.

    This function tries to call the `get_original_cwd` function from the `hydra.utils` module,
    which returns the original working directory if it exists. If the `get_original_cwd` function
    raises a `ValueError` exception, it means that Hydra did not change the working directory,
    so the function falls back to calling the `os.getcwd` function, which returns the current
    working directory.

    Returns:
        str: The original working directory before Hydra changed it.
    """
    try:
        return hydra.utils.get_original_cwd()
    except ValueError:
        return os.getcwd()


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
    # Set the context to the default context.
    if context is None:
        context = {}
    env = defaultdict(str, os.environ.copy())
    env.update(context)
    return Template(posix_expr).substitute(env)


def dotenv_values(dotenv_path=None, **kwargs):
    """Load dotenv file and return a dict of key/value pairs"""
    config = dotenv.dotenv_values(dotenv_path=dotenv_path, **kwargs)
    return dict(config)


def load_dotenv(
    override: bool = False,
    dotenv_dir: str = None,
    dotenv_filename: str = ".env",
    verbose: bool = False,
) -> None:
    """Load dotenv file from the given directory or from the current directory"""
    dotenv_dir = dotenv_dir or getcwd()
    dotenv_path = Path(dotenv_dir, dotenv_filename)
    if dotenv_path.is_file():
        dotenv.load_dotenv(dotenv_path=dotenv_path, verbose=verbose, override=override)
        os.environ["DOTENV_PATH"] = str(dotenv_path)
        os.environ["DOTENV_DIR"] = str(dotenv_path.parent)
        if verbose:
            logger.info("Loaded .env from %s", dotenv_path)
    else:
        if verbose:
            logger.info(
                "No .env file found in %s, finding .env in parent dirs", dotenv_path
            )
        if dotenv_path := dotenv.find_dotenv():
            dotenv.load_dotenv(
                dotenv_path=dotenv_path, verbose=verbose, override=override
            )
            os.environ["DOTENV_PATH"] = str(dotenv_path)
            os.environ["DOTENV_DIR"] = os.path.dirname(dotenv_path)
            if verbose:
                logger.info("Loaded .env from %s", dotenv_path)
        else:
            os.environ["DOTENV_PATH"] = ""
            os.environ["DOTENV_DIR"] = ""
            if verbose:
                logger.info("No .env file found in %s", dotenv_path)


def get_osenv(key: str = None, default: str = None) -> Any:
    """Get the value of an environment variable or return the default value"""
    load_dotenv()
    return os.environ.get(key, default) if key else os.environ


def set_osenv(key: str, value: Any) -> None:
    """Set the value of an environment variable"""
    if value and is_dir(value):
        value = os.path.abspath(value)
    if pre_val := os.environ.get(key):
        logger.info("Overwriting %s=%s with %s", key, pre_val, value)
    else:
        logger.info("Setting %s=%s", key, value)
    os.environ[key] = value

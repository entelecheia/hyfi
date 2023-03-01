"""Environment variable utilities"""
import os
from pathlib import Path
from typing import Any

import dotenv
import hydra

from ..io.file import is_dir
from .logging import getLogger

logger = getLogger(__name__)


def getcwd():
    """Get the original working directory before hydra changed it"""
    try:
        return hydra.utils.get_original_cwd()
    except ValueError:
        return os.getcwd()


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
        if verbose:
            logger.info("Loaded .env from %s", dotenv_path)
    else:
        if verbose:
            logger.info(
                "No .env file found in %s, finding .env in parent dirs", dotenv_path
            )
        dotenv_path = dotenv.find_dotenv()
        if dotenv_path:
            dotenv.load_dotenv(
                dotenv_path=dotenv_path, verbose=verbose, override=override
            )
            if verbose:
                logger.info("Loaded .env from %s", dotenv_path)
        else:
            if verbose:
                logger.info("No .env file found in %s", dotenv_path)


def get_osenv(key: str = None, default: str = None) -> Any:
    """Get the value of an environment variable or return the default value"""
    load_dotenv()
    if key:
        return os.environ.get(key, default)
    return os.environ


def set_osenv(key: str, value: Any) -> None:
    """Set the value of an environment variable"""
    if value and is_dir(value):
        value = os.path.abspath(value)
    pre_val = os.environ.get(key)
    if pre_val:
        logger.info("Overwriting %s=%s with %s", key, pre_val, value)
    else:
        logger.info("Setting %s=%s", key, value)
    os.environ[key] = value

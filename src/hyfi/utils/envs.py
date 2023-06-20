"""Environment variable utilities"""
import os
from collections import defaultdict
from pathlib import Path
from string import Template
from typing import Any, Union

import dotenv
import hydra

from hyfi.utils.iolibs import IOLibs
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


class Envs:
    @staticmethod
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

    @staticmethod
    def expand_posix_vars(posix_expr: str, context: dict = None) -> str:  # type: ignore
        # sourcery skip: dict-assign-update-to-union
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

    @staticmethod
    def dotenv_values(dotenv_path: str = "", **kwargs):
        """
        Load dotenv file and return a dict of key / value pairs. This is a wrapper around : py : func : ` dotenv. dotenv_values `

        Args:
            dotenv_path: path to. env file

        Returns:
            dict of key / value pairs ( key = value )
        """
        config = dotenv.dotenv_values(dotenv_path=dotenv_path, **kwargs)
        return dict(config)

    @staticmethod
    def load_dotenv(
        override: bool = False,
        dotenv_dir: str = "",
        dotenv_filename: str = ".env",
        verbose: bool = False,
    ) -> None:
        """
        Load. env file from given directory or from current directory. This is a convenience function for use in tests that want to run dotenv in a non - interactive environment

        Args:
            override: If True override existing. env file
            dotenv_dir: Directory to look for. env file ( default cwd )
            dotenv_filename: Name of. env file to look for
            verbose: Print debug information to console

        Returns:
            None or a Path object for the. env file
        """
        dotenv_dir = dotenv_dir or Envs.getcwd()
        dotenv_path = Path(dotenv_dir, dotenv_filename)
        # Load. env files and directories.
        if dotenv_path.is_file():
            dotenv.load_dotenv(
                dotenv_path=dotenv_path, verbose=verbose, override=override
            )
            os.environ["DOTENV_PATH"] = str(dotenv_path)
            os.environ["DOTENV_DIR"] = str(dotenv_path.parent)
            # Load. env from dotenv_path.
            if verbose:
                logger.info("Loaded .env from %s", dotenv_path)
            else:
                logger.debug("Loaded .env from %s", dotenv_path)
        else:
            # If verbose is true print out the. env file.
            if verbose:
                logger.info(
                    "No .env file found in %s, finding .env in parent dirs", dotenv_path
                )
            else:
                logger.debug(
                    "No .env file found in %s, finding .env in parent dirs", dotenv_path
                )
            # Load dotenv. env from dotenv.
            if dotenv_path := dotenv.find_dotenv():
                dotenv.load_dotenv(
                    dotenv_path=dotenv_path, verbose=verbose, override=override
                )
                os.environ["DOTENV_PATH"] = str(dotenv_path)
                os.environ["DOTENV_DIR"] = os.path.dirname(dotenv_path)
                # Load. env from dotenv_path.
                if verbose:
                    logger.info("Loaded .env from %s", dotenv_path)
                else:
                    logger.debug("Loaded .env from %s", dotenv_path)
            else:
                os.environ["DOTENV_PATH"] = ""
                os.environ["DOTENV_DIR"] = ""
                # Print out the. env file if verbose is true.
                if verbose:
                    logger.info("No .env file found in %s", dotenv_path)
                else:
                    logger.debug("No .env file found in %s", dotenv_path)

    @staticmethod
    def get_osenv(key: str = "", default: Union[str, None] = None) -> Any:
        """Get the value of an environment variable or return the default value"""
        Envs.load_dotenv()
        return os.environ.get(key, default) if key else os.environ

    @staticmethod
    def set_osenv(key: str, value: Any) -> None:
        """Set the value of an environment variable"""
        if value and IOLibs.is_dir(value):
            value = os.path.abspath(value)
        if pre_val := os.environ.get(key):
            logger.info("Overwriting %s=%s with %s", key, pre_val, value)
        else:
            logger.info("Setting %s=%s", key, value)
        os.environ[key] = value

    @staticmethod
    def check_and_set_osenv(key: str, value: Any) -> Any:
        """Check and set value to environment variable"""
        env_key = key.upper()
        if value is not None:
            old_value = os.getenv(env_key, "")
            if str(old_value).lower() != str(value).lower():
                os.environ[env_key] = str(value)
                logger.debug("Set environment variable %s=%s", env_key, str(value))
        return value

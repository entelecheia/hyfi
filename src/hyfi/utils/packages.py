"""This module provides utilities for loading library packages and dependencies."""
import importlib
import inspect
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from hyfi.utils.iolibs import IOLIBs
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class PKGs:
    @staticmethod
    def gitclone(
        url: str,
        targetdir: str = "",
        verbose: bool = False,
    ) -> None:
        """
        Clone a git repository from the specified URL.

        Args:
            url (str): The URL of the git repository to clone.
            targetdir (str, optional): The directory to clone the repository into. Defaults to "".
            verbose (bool, optional): Whether to print the output of the git command. Defaults to False.
        """
        if targetdir:
            res = subprocess.run(
                ["git", "clone", url, targetdir], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
        else:
            res = subprocess.run(
                ["git", "clone", url], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
        if verbose:
            print(res)
        else:
            logger.info(res)

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
    ) -> None:
        """
        Install a package using pip.

        Args:
            name (str): The name of the package to install.
            upgrade (bool, optional): Whether to upgrade the package if it is already installed. Defaults to False.
            prelease (bool, optional): Whether to include pre-release versions. Defaults to False.
            editable (bool, optional): Whether to install the package in editable mode. Defaults to False.
            quiet (bool, optional): Whether to suppress output. Defaults to True.
            find_links (str, optional): URL to look for packages at. Defaults to "".
            requirement (bool, optional): Whether to install from the given requirements file. Defaults to False.
            force_reinstall (bool, optional): Whether to force a reinstall of the package. Defaults to False.
            verbose (bool, optional): Whether to print the output of the pip command. Defaults to False.
            **kwargs: Additional keyword arguments to pass to pip.

        Returns:
            None
        """
        _cmd = ["pip", "install"]
        if upgrade:
            _cmd.append("--upgrade")
        if prelease:
            _cmd.append("--pre")
        if editable:
            _cmd.append("--editable")
        if quiet:
            _cmd.append("--quiet")
        if find_links:
            _cmd += ["--find-links", find_links]
        if requirement:
            _cmd.append("--requirement")
        if force_reinstall:
            _cmd.append("--force-reinstall")
        for k in kwargs:
            k = k.replace("_", "-")
            _cmd.append(f"--{k}")
        _cmd.append(name)
        if verbose:
            logger.info(f"Installing: {' '.join(_cmd)}")
        res = subprocess.run(_cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
        if verbose:
            print(res)
        else:
            logger.info(res)

    @staticmethod
    def pipi(name: str, verbose: bool = False) -> None:
        """Install a package using pip."""
        res = subprocess.run(
            ["pip", "install", name], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
        if verbose:
            print(res)
        else:
            logger.info(res)

    @staticmethod
    def pipie(name: str, verbose: bool = False) -> None:
        """Install a editable package using pip."""
        res = subprocess.run(
            ["git", "install", "-e", name], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
        if verbose:
            print(res)
        else:
            logger.info(res)

    @staticmethod
    def apti(name: str, verbose: bool = False) -> None:
        """Install a package using apt."""
        res = subprocess.run(
            ["apt", "install", name], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
        if verbose:
            print(res)
        else:
            logger.info(res)

    @staticmethod
    def load_module_from_file(name: str, libpath: str, specname: str = "") -> None:
        """Load a module from a file"""
        module_path = os.path.join(libpath, name.replace(".", os.path.sep))
        if IOLIBs.is_file(f"{module_path}.py"):
            module_path = f"{module_path}.py"
        elif IOLIBs.is_dir(module_path):
            module_path = os.path.join(module_path, "__init__.py")
        else:
            module_path = str(Path(module_path).parent / "__init__.py")

        spec = importlib.util.spec_from_file_location(name, module_path)  # type: ignore
        module = importlib.util.module_from_spec(spec)  # type: ignore
        if not specname:
            specname = spec.name
        sys.modules[specname] = module
        spec.loader.exec_module(module)

    @staticmethod
    def ensure_import_module(
        name: str,
        libpath: str,
        liburi: str,
        specname: str = "",
        syspath: str = "",
    ) -> None:
        """Ensure a module is imported, if not, clone it from a git repo and load it"""
        try:
            if specname:
                importlib.import_module(specname)
            else:
                importlib.import_module(name)
            logger.info(f"{name} imported")
        except ImportError:
            if not os.path.exists(libpath):
                logger.info(f"{libpath} not found, cloning from {liburi}")
                PKGs.gitclone(liburi, libpath)
            if not syspath:
                syspath = libpath
            if syspath not in sys.path:
                sys.path.append(syspath)
            PKGs.load_module_from_file(name, syspath, specname)
            specname = specname or name
            logger.info(f"{name} not imported, loading from {syspath} as {specname}")

    @staticmethod
    def getsource(obj: str) -> str:
        """
        Return the source code of the object.

        Args:
            obj (str): The object to get the source code from.

        Returns:
            str: The source code of the object.

        """
        try:
            mod_name, object_name = obj.rsplit(".", 1)
            mod = importlib.import_module(mod_name)
            obj_ = getattr(mod, object_name)
            return inspect.getsource(obj_)
        except Exception as e:
            logger.error(f"Error getting source: {e}")
            return ""

    @staticmethod
    def viewsource(obj: str) -> None:
        """Print the source code of the object."""
        print(PKGs.getsource(obj))

    @staticmethod
    def get_caller_module_name(caller_stack_depth: int = 2) -> str:
        """Get the name of the module that called this function."""
        try:
            _stack = inspect.stack()
            if len(_stack) < caller_stack_depth + 1:
                logger.info(
                    "Returning top level module name (depth %d)", len(_stack) - 1
                )
                return inspect.getmodule(_stack[-1][0]).__name__  # type: ignore
            return inspect.getmodule(_stack[caller_stack_depth][0]).__name__  # type: ignore
        except Exception as e:
            logger.error(
                f"Error getting caller module name at depth {caller_stack_depth}: {e}"
            )
            return ""

    @staticmethod
    def is_importable(module_name: str) -> bool:
        module_spec = importlib.util.find_spec(module_name)  # type: ignore
        return module_spec is not None

    @staticmethod
    def safe_import_module(module_name: str) -> Any:
        """Safely imports a module."""
        try:
            return importlib.import_module(module_name)
        except ImportError:
            logger.debug("Failed to import module: %s", module_name)
            return None

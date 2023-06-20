"""Utilities for loading library packages and dependencies."""
import importlib
import os
import subprocess
import sys
from pathlib import Path

from hyfi.utils.iolibs import IOLibs
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


class Packages:
    @staticmethod
    def gitclone(
        url: str,
        targetdir: str = "",
        verbose: bool = False,
    ) -> None:
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
        """Install a package using pip."""
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
        if IOLibs.is_file(f"{module_path}.py"):
            module_path = f"{module_path}.py"
        elif IOLibs.is_dir(module_path):
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
                Packages.gitclone(liburi, libpath)
            if not syspath:
                syspath = libpath
            if syspath not in sys.path:
                sys.path.append(syspath)
            Packages.load_module_from_file(name, syspath, specname)
            specname = specname or name
            logger.info(f"{name} not imported, loading from {syspath} as {specname}")

"""cached download and extract archive"""
from pathlib import Path

import gdown

from hyfi.cached_path import _cached_path

from .iolibs import IOLIBs
from .logging import LOGGING

logger = LOGGING.getLogger(__name__)


class CACHED:
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
        if not url_or_filename:
            logger.warning("url_or_filename not provided")
            return None
        if verbose:
            logger.info(
                "caching path: %s, extract_archive: %s, force_extract: %s, cache_dir: %s",
                url_or_filename,
                extract_archive,
                force_extract,
                cache_dir,
            )

        try:
            if url_or_filename.startswith("gd://"):
                _path = IOLIBs.cached_gdown(
                    url_or_filename,
                    verbose=verbose,
                    extract_archive=extract_archive,
                    force_extract=force_extract,
                    cache_dir=cache_dir,
                )
                _path = Path(_path) if isinstance(_path, str) else None
            else:
                if _cached_path is None:
                    raise ImportError(
                        "Error importing required libraries 'cached-path'. "
                        "Please install them using 'pip install cached-path' and try again."
                    )

                if cache_dir:
                    cache_dir = str(Path(cache_dir) / "cached_path")
                else:
                    cache_dir = str(Path.home() / ".hyfi" / ".cache" / "cached_path")

                _path = _cached_path.cached_path(
                    url_or_filename,
                    extract_archive=extract_archive,
                    force_extract=force_extract,
                    cache_dir=cache_dir,
                )

            logger.debug("cached path: %s", _path)

            if _path and _path.is_file():
                _parent_dir = Path(_path).parent
            elif _path and _path.is_dir():
                _parent_dir = Path(_path)
            else:
                logger.warning("Unknown path: %s", _path)
                return None

            return _parent_dir.as_posix() if return_parent_dir else _path
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def cached_gdown(
        url: str,
        verbose: bool = False,
        extract_archive: bool = False,
        force_extract: bool = False,
        cache_dir: str = "",
    ):
        """
        :type url: str
            ex) gd://id:path
        :type verbose: bool
        :type extract_archive: bool
        :type force_extract: bool
        :type cache_dir: str
        :returns: str
        """
        if gdown is None:
            raise ImportError(
                "Error importing required libraries 'gdown'. "
                "Please install them using 'pip install gdown' and try again."
            )

        if verbose:
            logger.info("Downloading %s...", url)
        if cache_dir:
            cache_dir_ = Path(cache_dir) / "gdown"
        else:
            cache_dir_ = Path.home() / ".hyfi" / ".cache" / "gdown"
        cache_dir_.mkdir(parents=True, exist_ok=True)

        gd_prefix = "gd://"
        if url.startswith(gd_prefix):
            url = url[len(gd_prefix) :]
            _url = url.split(":")
            if len(_url) == 2:
                id_, path = _url
            else:
                id_ = _url[0]
                path = id_

            # If we're using the path!c/d/file.txt syntax, handle it here.
            fname = None
            extraction_path = path
            exclamation_index = path.find("!")
            if extract_archive and exclamation_index >= 0:
                extraction_path = path[:exclamation_index]
                fname = path[exclamation_index + 1 :]

            cache_path = cache_dir_ / f".{id_}" / extraction_path
            cache_path.parent.mkdir(parents=True, exist_ok=True)

            cache_path = gdown.cached_download(
                id=id_,
                path=cache_path.as_posix(),
                quiet=not verbose,
            )

            if extract_archive:
                extraction_path, files = IOLIBs.extractall(
                    cache_path, force_extract=force_extract
                )

                if not fname or not files:
                    return extraction_path
                for f in files:
                    if f.endswith(fname):
                        return f
            return cache_path

        else:
            logger.warning("Unknown url: %s", url)
            return None

"""Logging utilities"""
import logging
import os
import sys
import warnings


class LOGGING:
    @staticmethod
    def setLogger(
        level=None,
        force=True,
        filterwarnings_action="ignore",
        **kwargs,
    ) -> None:
        """
        Set the logging level and format. This is a wrapper around logging. basicConfig to allow the user to specify a different logging level for each test and to filter warnings that are not caught by the filterwarnings_action

        Args:
            level: The logging level to use
            force: If True ( default ) all warnings will be logged even if there are no warnings
            filterwarnings_action: The action to call when a warning is logged

        Returns:
            The logger that was
        """
        level = level or os.environ.get("HYFI_LOG_LEVEL") or "INFO"
        level = level.upper()
        os.environ["HYFI_LOG_LEVEL"] = level
        # Filter warnings by applying filterwarnings_action to the warnings.
        if filterwarnings_action is not None:
            warnings.filterwarnings(filterwarnings_action)  # type: ignore
        # Return the logging level.
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        # Configure logging level level and force logging.
        if sys.version_info >= (3, 8):
            logging.basicConfig(level=level, force=force, **kwargs)
        else:
            logging.basicConfig(level=level, **kwargs)

    @staticmethod
    def getLogger(
        _name=None,
        _log_level=None,
        **kwargs,
    ) -> logging.Logger:
        """
        Get a logger with a given name and log level. It is possible to pass a logger name and log level to this function.

        Args:
            _name: The name of the logger to get. If not specified the name of the module is used.
            _log_level: The log level to set.

        Returns:
            The logger with the given name and log level set to the value specified in HYFI_LOG_LEVEL
        """
        _name = _name or __name__
        logger = logging.getLogger(_name)
        _log_level = _log_level or os.environ.get("HYFI_LOG_LEVEL") or "INFO"
        logger.setLevel(_log_level)
        return logger

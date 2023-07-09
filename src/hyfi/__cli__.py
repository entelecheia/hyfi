"""Command line interface for HyFI"""
import os
from typing import Optional

import hydra
from omegaconf import DictConfig

from hyfi.__global__ import __about__, __hydra_version_base__
from hyfi.__global__.config import HyfiConfig
from hyfi.main import HyFI
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


__config_path__ = "conf"
__config_name__ = "config"


def about(**args):
    """
    Print the about information for Hyfi.
    This is a wrapper around _about which takes a HyfiConfig as an argument
    """
    HyFI.run(args)


def run_copy(**args):
    """
    Copy all config files to the current working directory.
    This is a wrapper around HyfiConfig to allow us to pass arguments to it.
    """
    HyFI.run(args, "copier")


def run_task(**args):
    """
    Run a task. This is a wrapper around HyFI
    """
    HyFI.run(args, "task")


def run_workflow(**args):
    """
    Run a workflow. This is a wrapper around HyFI. run_workflow
    """
    HyFI.run(args, "workflow")


def cli_main(cfg: DictConfig) -> None:
    """
    Main function for the command line interface.
    Initializes Hydra and instantiates the class.
    Prints the configuration to standard out if verbose is set to True

    Args:
        cfg: Configuration dictionary to be used for instantiation

    Returns:
        None if everything went fine otherwise an error is raised
        to indicate the reason for the failure
    """
    hyfi = HyfiConfig(**cfg)  # type: ignore
    verbose = hyfi.verbose
    # Print out the command line interface for the application.
    if verbose:
        app_name = hyfi.app_name
        print(f"## Command Line Interface for {app_name} ##")

        # Prints the configuration to the console.
        if hyfi.resolve:
            logger.info("## hydra configuration resolved ##")
            HyFI.print(cfg)
        else:
            logger.info("## hydra configuration ##")
            print(HyFI.to_yaml(cfg))

        logger.info("Hydra working directory : %s", {os.getcwd()})
        logger.info("Orig working directory  : %s", {hydra.utils.get_original_cwd()})

    if HyFI.is_instantiatable(cfg):
        HyFI.instantiate(cfg)
    else:
        hyfi.run()

    HyFI.terminate()


def hydra_main(
    config_path: Optional[str] = __config_path__,
    config_name: Optional[str] = __config_name__,
) -> None:
    """
    Main function for the command line interface of Hydra

    Args:
        config_path: The config path, a directory where Hydra will search for
                        config files. This path is added to Hydra's searchpath.
                        Relative paths are interpreted relative to the declaring python
                        file. Alternatively, you can use the prefix `pkg://` to specify
                        a python package to add to the searchpath.
                        If config_path is None no directory is added to the Config search path.
        config_name: The name of the config (usually the file name without the .yaml extension)
    """
    # Returns the path to the config file.
    if config_path is None:
        config_path = __about__.config_path
    hydra.main(
        config_path=config_path,
        config_name=config_name,
        version_base=__hydra_version_base__,
    )(cli_main)()

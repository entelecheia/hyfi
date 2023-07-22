"""Command line interface for HyFI"""
import os
import sys
from typing import List, Optional

import hydra
from omegaconf import DictConfig

from hyfi.core import __global_hyfi__, __hydra_version_base__, __hyfi_package_name__
from hyfi.core.config import HyfiConfig
from hyfi.core.hydra.main import main as hyfi_hydra_main
from hyfi.main import HyFI

logger = HyFI.getLogger(__name__)


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
    HyFI.initialize()
    hyfi = HyfiConfig(**cfg)  # type: ignore
    if hyfi.project:
        HyFI.set_project(hyfi.project)

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

        logger.info("Hydra working directory : %s", os.getcwd())
        logger.info("Orig working directory  : %s", hydra.utils.get_original_cwd())

    HyFI.run_config(config=cfg)

    HyFI.terminate()


def hyfi_main(
    config_path: Optional[str] = None,
    config_name: Optional[str] = None,
    overrides: Optional[List[str]] = None,
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
    if search_path := __global_hyfi__.user_config_path:
        sys.argv.append(f"--config-dir={search_path}")
    if not config_path:
        config_path = __global_hyfi__.config_module_path
    if not config_name:
        config_name = __global_hyfi__.config_name
    if __global_hyfi__.__package_name__ != __hyfi_package_name__:
        overrides = overrides or []
        override = f"about={__global_hyfi__.__package_name__}"
        if override not in overrides:
            overrides.append(override)
            logger.debug(
                "Overriding `about` config group with `%s`",
                __global_hyfi__.__package_name__,
            )
    hyfi_hydra_main(
        config_path=config_path,
        config_name=config_name,
        version_base=__hydra_version_base__,
        overrides=overrides,
    )(cli_main)()


def hydra_main(
    config_path: Optional[str] = None,
    config_name: Optional[str] = None,
    overrides: Optional[List[str]] = None,
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
    hyfi_main(config_path, config_name, overrides)

"""Command line interface for HyFI"""
import os
from typing import Optional

import hydra

from .env import HyfiConfig, __about__, __hydra_version_base__
from .main import DictConfig, HyFI, _about, getLogger
from .utils.copier import Copier

logger = getLogger(__name__)


__config_path__ = "conf"
__config_name__ = "config"


def cmd(**args):
    """Run the command defined in the config file"""
    HyFI.run(args)


def about(**args):
    """Print the about information"""
    cfg = HyfiConfig(**args)
    _about(cfg)


def run_copy(**args):
    """Copy all config files in the config directory to the current working directory"""
    cfg = HyfiConfig(**args)
    cfg = HyFI.to_dict(cfg.copier)
    with Copier(**cfg) as worker:
        worker.run_copy()


def cli_main(cfg: DictConfig) -> None:
    """Main function for the command line interface"""
    hyfi = HyfiConfig(**cfg)
    verbose = hyfi.verbose
    app_name = hyfi.about.name
    print_config = hyfi.print_config
    print_resolved_config = hyfi.print_resolved_config

    if verbose:
        print("## Command Line Interface for %s ##" % app_name)
    HyFI.initialize(cfg)

    if print_config:
        if print_resolved_config:
            logger.info("## hydra configuration resolved ##")
            HyFI.pprint(cfg)
        else:
            logger.info("## hydra configuration ##")
            print(HyFI.to_yaml(cfg))

    if verbose:
        logger.info(f"Hydra working directory : {os.getcwd()}")
        logger.info(f"Orig working directory  : {hydra.utils.get_original_cwd()}")

    HyFI.instantiate(cfg)

    HyFI.terminate()


def hydra_main(
    config_path: Optional[str] = __config_path__,
    config_name: Optional[str] = __config_name__,
) -> None:
    """
    Main function for the command line interface of Hydra
    :param config_path: The config path, a directory where Hydra will search for
                        config files. This path is added to Hydra's searchpath.
                        Relative paths are interpreted relative to the declaring python
                        file. Alternatively, you can use the prefix `pkg://` to specify
                        a python package to add to the searchpath.
                        If config_path is None no directory is added to the Config search path.
    :param config_name: The name of the config (usually the file name without the .yaml extension)
    """
    if config_path is None:
        config_path = __about__.config_path
    hydra.main(
        config_path=config_path,
        config_name=config_name,
        version_base=__hydra_version_base__,
    )(cli_main)()


if __name__ == "__main__":
    """Run the command line interface"""
    hydra_main()

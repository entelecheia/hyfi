"""Command line interface for HyFI"""
import os

import click

from hyfi._version import __version__
from hyfi.env import HyfiConfig, __about__, __hydra_version_base__
from hyfi.main import HyFI, _about, getLogger

logger = getLogger(__name__)


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
@click.option("--src_path", default="conf", help="Source path to copy from")
@click.option("--dst_path", default=".", help="Destination path to copy to")
@click.option("--exclude", default=None, help="Exclude files matching this pattern")
@click.option("--skip_if_exists", default=False, help="Skip if destination exists")
@click.option("--overwrite", default=False, help="Overwrite destination")
@click.option("--dry_run", default=False, help="Dry run")
@click.option("--verbose", default=False, help="Verbose output")
def cc(**args):
    """
    Copy all config files to the destination directory.
    """
    click.echo("Copying configuration files")
    click.echo(f"args : {args}")


@cli.command()
def about():
    """
    Print the about information for Hyfi.
    """
    cfg = HyfiConfig()
    _about(cfg)


@cli.command()
@click.option(
    "--uninstall", is_flag=True, default=False, help="Uninstall shell completion"
)
@click.option("--shell", default="zsh", help="Shell to install completion for")
def sc(uninstall, shell):
    """
    Install or Uninstall shell completion for Hyfi.
    """
    if uninstall:
        click.echo(f"Uninstall shell completion for {shell}:")
        click.echo(
            "run the following command to uninstall shell completion in your current shell\n"
        )
        click.echo(f'eval "$(hyfi -sc uninstall={shell})"')
    else:
        click.echo(f"Install shell completion for {shell}:")
        click.echo(
            "run the following command to install shell completion in your current shell\n"
        )
        click.echo(f'eval "$(hyfi -sc install={shell})"')

"""Command line interface for HyFI"""

import click

from hyfi.__global__ import __hyfi_path__
from hyfi.__global__.config import HyfiConfig
from hyfi._version import __version__
from hyfi.copier import Copier
from hyfi.main import _about
from hyfi.utils.logging import Logging

logger = Logging.getLogger(__name__)


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
@click.option(
    "--src_path",
    show_default=True,
    default=f"{__hyfi_path__()}/conf",
    help="Source path to copy from",
)
@click.option(
    "--dst_path",
    show_default=True,
    default="./tmp/conf",
    help="Destination path to copy to",
)
@click.option(
    "--exclude",
    show_default=True,
    default=None,
    help="Exclude files matching this pattern",
)
@click.option(
    "--skip_if_exists",
    is_flag=True,
    show_default=True,
    default=False,
    help="Skip if destination exists",
)
@click.option(
    "--overwrite",
    is_flag=True,
    show_default=True,
    default=False,
    help="Overwrite destination",
)
@click.option(
    "--dry_run", is_flag=True, show_default=True, default=False, help="Dry run"
)
@click.option(
    "--verbose", is_flag=True, show_default=True, default=False, help="Verbose output"
)
def cc(**args):
    """
    Copy all config files to the destination directory.
    """
    click.echo("Copying configuration files")
    # click.echo(f"args : {args}")
    with Copier(**args) as worker:
        worker.run_copy()


@cli.command()
def about():
    """
    Print the about information for Hyfi.
    """
    cfg = HyfiConfig()
    cfg.about.version = __version__
    _about(cfg)


@cli.command()
@click.option(
    "--uninstall",
    "-u",
    is_flag=True,
    show_default=True,
    default=False,
    help="Uninstall shell completion",
)
@click.option(
    "--shell",
    "-s",
    show_default=True,
    default="zsh",
    help="Shell to install completion for",
)
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

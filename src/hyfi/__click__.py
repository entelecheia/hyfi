"""Command line interface for HyFI"""

import click

from hyfi._version import __version__
from hyfi.copier import Copier
from hyfi.core import global_hyfi
from hyfi.main import HyFI, HyfiConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
@click.option(
    "--config",
    "-c",
    show_default=True,
    help="Config group to compose and run",
)
@click.option(
    "--print",
    "-p",
    show_default=True,
    is_flag=True,
    default=False,
    help="Print the configuration instead of running it",
)
@click.pass_context
def cli(ctx, config: str, print: bool):
    """This is the auxiliary command line interface for Hyfi. The main command line
    interface is 'hyfi'.

    It is used to help run HyFI applications. If no command is specified, it will
    compose a configuration and run it.

    It is also used to copy configuration files to the destination directory and
    to install shell completion for Hyfi.
    \f

    :param click.core.Context ctx: Click context.
    """
    if ctx.invoked_subcommand is None:
        if config:
            if print:
                HyFI.print_config(config)
            else:
                HyFI.run(config_group=config)
        else:
            click.echo(ctx.get_help())


@cli.command()
@click.option(
    "--src_path",
    show_default=True,
    default=f"{global_hyfi.hyfi_package_name}/{global_hyfi.hyfi_config_dirname}",
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
    HyfiConfig().print_about()


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

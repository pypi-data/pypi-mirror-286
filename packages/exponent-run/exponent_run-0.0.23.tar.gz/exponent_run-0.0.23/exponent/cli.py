import click

from exponent.commands.cloud_commands import (
    cloud_cli,
)
from exponent.commands.common import (
    set_log_level,
)
from exponent.commands.config_commands import config_cli
from exponent.commands.run_commands import run_cli
from exponent.commands.shell_commands import shell_cli
from exponent.commands.utils import check_exponent_version
from exponent.core.config import is_editable_install
from exponent.version import get_version


@click.group()
@click.version_option(get_version(), prog_name="Exponent CLI")
def exponent_cli() -> None:
    """Exponent CLI group."""
    set_log_level()
    if not is_editable_install():
        check_exponent_version()


cli = click.CommandCollection(
    sources=[exponent_cli, config_cli, run_cli, shell_cli, cloud_cli]
)

if __name__ == "__main__":
    cli()

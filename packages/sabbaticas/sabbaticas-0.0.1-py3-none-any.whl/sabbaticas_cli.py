# sabbaticas_cli.py
import click
from prettytable import PrettyTable

@click.group()
def cli():
    """sabbaticas is a tool for assessing software security practices.
    
    For documentation on how commands run `sabbaticas COMMAND --help`.

    """

@cli.command("assess")
@click.argument('directory', required=False, type=click.Path(exists=True))
def assess(directory):
    """Assess a directory."""
    click.echo()
    if directory:
        click.echo(f'Assessing directory: {directory}')
    else:
        click.echo('Assessing current directory.')
        directory = "."

@cli.command("version")
def version():
    """Print the version of sabbatics."""
    click.echo("sabbatiacs version 0.0.1")

if __name__ == '__main__':
    cli()

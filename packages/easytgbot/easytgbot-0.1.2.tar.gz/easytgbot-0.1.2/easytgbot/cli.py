import click
import os

from .utils.utils import initialize_all_files_from_drafts


@click.group()
@click.version_option()
def cli():
    """The CLI tool."""


@cli.command()
def run():
    if initialize_all_files_from_drafts():
        os.system("poetry run python main.py")


# Developer mode
if __name__ == "__main__":
    cli()

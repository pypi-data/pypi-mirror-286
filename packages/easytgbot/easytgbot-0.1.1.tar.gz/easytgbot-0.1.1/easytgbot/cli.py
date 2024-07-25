import click
import os
import shutil

from .mylogging import logger


@click.group()
@click.version_option()
def cli():
    """The CLI tool."""


@cli.command()
def run():
    if init():
        os.system("poetry run python main.py")


def init():
    """
    This command checks if 'main.py', '.env', and 'text.xlsx' 
    exist in the current working directory, 
    if not they are created from their respective example files,
    and finally main.py is launched.
    """
    file = ".env"
    example_file = "easytgbot/.env.example"

    if not os.path.exists(file):
        shutil.copy(example_file, file)
        logger.info(f"{file} file created. Please fill it and try again.")
        return 
    
    files_to_check = {
        "text.xlsx": "easytgbot/text_example.xlsx",
        "main.py": "easytgbot/main_example.py",
    }

    for file, example_file in files_to_check.items():
        if not os.path.exists(file):
            shutil.copy(example_file, file)
            logger.info(f"{file} file created.")
    
    return True


# Developer mode
if __name__ == "__main__":
    cli()

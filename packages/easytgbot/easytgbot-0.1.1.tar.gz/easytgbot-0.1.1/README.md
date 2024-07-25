# Easy Telegram Bot - **easytgbot**

This is my own Telegram bot framework for the faster development, and updating already existing projects.

Based on [Python Telegram Bot](https://docs.python-telegram-bot.org/en/v21.4/).

## Features

### Register commands with a decorator

```python
from mytgbot import command

@command()
async def help(update, context):
    pass
```

...


## Installation & Usage

This is an installable Python package.

### PyPI

0. `poetry add mytgbot3719` or `pip install mytgbot3719`
1. `easytgbot run`

### PowerShell

Make sure poetry is installed. From this folder,

0. `poetry shell; poetry update;`

1. `poetry build; poetry install;`

2. `easytgbot run`

In the bot if run is successful,

`/admin`

Ctrl+C to exit.

`easytgbot run` command runs "main.py" file, so one can as well run it directly. 

## # TODO

- `/admin` -> *edit text file*

- `/intro_vid` -> *add intro video*

- `/admin` -> *add peope* -> (*add admin*, *add user*) -> if list of users does not exist, create one and lock the access to the bot with the current users

- `/superadmin` -> *get db*

- `/superadmin` -> *bot up/down*

- `/start`

### Default Bot Commands

By default, in the bot

- `/start` command makes a user chose a language
- then it makes a user agree to the terms and conditions
- through `/admin` -> "⚙️ ...", admins regulate all the text of the bot via exel file manipulation
- all the bot text is stored in an exel file `text.xlsx` with "string_text_key":"value" structure, and the columns are the languages.
- logs are rotating automatically

To add a text, simply add a unique text index and the corresponding value in at least one language in the `text.xlsx`.
The first column has to be complete always as a main language.
All the text info is preserved in the bot persistance.

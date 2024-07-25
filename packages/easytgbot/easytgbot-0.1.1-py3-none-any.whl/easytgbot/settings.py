import os
from dotenv import load_dotenv

load_dotenv(override=True)


def get_secret_by_name(name: str):
    return os.getenv(name)


# TG creds
BOT_NAME = get_secret_by_name("TG_BOT_NAME")
TG_BOT_TOKEN = get_secret_by_name("TG_BOT_TOKEN")

# Tg IDs
MY_TG_ID = str(get_secret_by_name("MY_TG_ID"))

SUPERADMIN_GROUP = [MY_TG_ID]
ADMIN_GROUP = []

__version__ = "0.1.0"

# Add handlers to the application, run polling
from .app import application, telegram_bot_polling

# Add command handlers with
from .decorators import command

from .send import send_text

from .admin import is_user_admin


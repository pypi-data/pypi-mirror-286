from easytgbot import command, send_text, telegram_bot_polling


@command()
async def help(update, context):
    return await send_text(update, context, "help_message")


if __name__=="__main__":
    telegram_bot_polling()

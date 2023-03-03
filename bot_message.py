#send matches as telegram message
import telegram
import config


def telegram_bot_sendtext(bot_message):

    bot = telegram.Bot(token=config.bot_token)
    if bot_message:
        bot.send_message(chat_id=config.bot_chatID, text=bot_message)

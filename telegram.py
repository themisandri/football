#send matches as telegram message
import telegram

def telegram_bot_sendtext(bot_message):
    
    bot_token = '5747201168:AAGxiQ3yrr884aQKHnwn-VIpI9d1w_pQAnY'
    bot_chatID = '-874589090'
    bot = telegram.Bot(token=bot_token)
    bot.sendMessage(chat_id=bot_chatID, text=bot_message)


import os
from dotenv import load_dotenv
import telebot

load_dotenv()

bot_TOKEN = os.getenv("BOT_TOKEN")
BOT = telebot.TeleBot(bot_TOKEN)

@BOT.message_handler(commands=['start'])
def start(message):
    BOT.send_message(message.chat.id, "Hello i am Sleep_bot, chose command\n")
    BOT.send_message(message.chat.id, f"/Insert\n/Get\n/Stats")


#BOT.polling()



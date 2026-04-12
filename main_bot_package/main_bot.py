import os
from dotenv import load_dotenv
import telebot
from telebot import types
from telebot_functions import create_keyboard_panel

load_dotenv()

bot_TOKEN = os.getenv("BOT_TOKEN")
BOT = telebot.TeleBot(bot_TOKEN)

@BOT.message_handler(commands=['start'])
def start(message):
    BOT.send_message(message.chat.id, "Hello i am Sleep_bot\n")
    markup = create_keyboard_panel()

    BOT.send_message(
       message.chat.id,
       "Chose a command 👇",
        reply_markup=markup
    )


BOT.polling()



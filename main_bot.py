import os
from dotenv import load_dotenv
import telebot
from main_bot_package.telebot_functions import create_keyboard_panel
from main_bot_package.file_date_functions import save_file

load_dotenv()  #loading .env

bot_TOKEN = os.getenv("BOT_TOKEN")
BOT = telebot.TeleBot(bot_TOKEN)


def load_data(message):
    try:
        save_file(message)
        BOT.send_message(message.chat.id, "Text was added successfully")

    except TypeError:
        BOT.send_message(message.chat.id, "You have to send a text, try again")
        BOT.register_next_step_handler(message, load_data)


@BOT.message_handler(commands=['start'])
def start(message):
    BOT.send_message(message.chat.id, "Hello i am Sleep_bot\n")
    markup = create_keyboard_panel()

    BOT.send_message(
       message.chat.id,
       "Chose a command 👇",
        reply_markup=markup
    )

@BOT.message_handler(content_types=['photo', 'voice'])
def handle_all(message):

    BOT.send_message(
        message.chat.id,
        "Sorry, bot doesn't support photo or voice, use please these commands👇",
        reply_markup=create_keyboard_panel()
    )


@BOT.message_handler(func=lambda message: True)
def reaction_to_button(message):
    if message.text not in ["📁 My files", "📤 Upload",
                            "🗑️ Delete", "🔎 Search", "❓ Help"]:

        BOT.send_message(
            message.chat.id,
            "Sorry, currently are only those commands into use👇",
            reply_markup=create_keyboard_panel()
        )

    if message.text == "📤 Upload":
        BOT.send_message(message.chat.id, "Good, so now send a text so i can save it")
        BOT.register_next_step_handler(message, load_data)





#BOT.polling()



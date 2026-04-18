import os
from dotenv import load_dotenv
import telebot
from main_bot_package.telebot_functions import create_keyboard_panel
from main_bot_package.file_date_functions import save_file

load_dotenv()  #loading .env

bot_TOKEN = os.getenv("BOT_TOKEN")
BOT = telebot.TeleBot(bot_TOKEN)
COMMANDS = ["📁 My files", "📤 Upload", "🗑️ Delete", "🔎 Search", "❓ Help"]


def load_data(message):
    try:
        if message.content_type in ['voice', 'video_note', 'photo']:  #currently takes text, documents only.
            raise TypeError

        elif message.text:
            save_file(message.from_user.id, text=message.text)
            BOT.send_message(message.chat.id, "Text was saved successfully✅")

        elif message.document:
            BOT.send_message(message.chat.id, "Got it, may take a lil time⌛ to save it")
            file_id = message.document.file_id
            file_info = BOT.get_file(file_id)
            downloaded_bytes = BOT.download_file(file_info.file_path)
            save_file(message.from_user.id, file_bytes=downloaded_bytes, file_name=message.document.file_name)
            BOT.send_message(message.chat.id, "File was saved successfully✅")

    except TypeError:
        BOT.send_message(message.chat.id, "Currently are only text and documents allowed, try again")
        BOT.register_next_step_handler(message, load_data)


@BOT.message_handler(commands=['start'])
def start(message):
    BOT.send_message(message.chat.id, "Hello i am bot for working with text, and files\n")
    markup = create_keyboard_panel()

    BOT.send_message(
       message.chat.id,
       "Chose a command ⤵️",
        reply_markup=markup
    )

@BOT.message_handler(func=lambda message: message.text in COMMANDS)
def reaction_to_button(message):
    if message.text == "📤 Upload":
        BOT.send_message(message.chat.id, "Good, so now send a text or file so i can save it📁")
        BOT.register_next_step_handler(message, load_data)

#filtration👇
@BOT.message_handler(func=lambda message: True, content_types=['text', 'photo', 'voice', 'document', 'video_note'])
def handle_not_supported(message):
    BOT.send_message(
        message.chat.id,
        "No such option, use one of those⤵️",
        reply_markup=create_keyboard_panel()
    )






BOT.polling()



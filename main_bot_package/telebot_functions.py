"""Well this file was created for a case if the code should to repeat itself,
so i kep my code clean."""
import os

from telebot import types
from os import scandir
def create_keyboard_panel():
    """Making a keyboard, for a '/start' command,
    also will be used in cases if user sends voice, or video message(wrong format)
    or everything what causes error."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    file_btn = types.KeyboardButton("📁 My files")
    upload_btn = types.KeyboardButton("📤 Upload")
    del_btn = types.KeyboardButton("🗑️ Delete")
    help_btn = types.KeyboardButton("❓ Help")
    markup.add(file_btn, upload_btn)
    markup.add(del_btn, help_btn)
    return markup

def inline_buttons(dir_path: str, month_dirs: bool = False):
    keyboard = types.InlineKeyboardMarkup()
    if month_dirs:
        for month_dir in os.listdir(dir_path):
            call_back = f"month_dir:{month_dir}"
            keyboard.add(types.InlineKeyboardButton(f"Show: 📁 {month_dir}", callback_data=call_back))

        return keyboard


    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_dir():
                call_back = f"data_dir:{entry.name}"
                keyboard.add(types.InlineKeyboardButton(f"Show me:📁 {entry.name}", callback_data=call_back))


            else:
                call_back = f"send:{entry.name}"
                keyboard.add(types.InlineKeyboardButton(f"Send me:📄 {entry.name}", callback_data=call_back))

    return keyboard


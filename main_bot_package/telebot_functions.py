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
    search_btn = types.KeyboardButton("🔎 Search")
    help_btn = types.KeyboardButton("❓ Help")
    markup.add(file_btn, upload_btn)
    markup.add(del_btn, search_btn)
    markup.add(help_btn)
    return markup

def inline_buttons(dir_path: str, month_dirs: bool = False):
    keyboard = types.InlineKeyboardMarkup()
    if month_dirs:
        for month_dir in os.listdir(dir_path):
            call_back = f"month_dir:{month_dir}"
            keyboard.add(types.InlineKeyboardButton(f"Show: 📁 {month_dir}", callback_data=call_back))

        return keyboard


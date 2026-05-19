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
    back_btn = types.KeyboardButton("Back⬇️")
    markup.add(file_btn, upload_btn)
    markup.add(del_btn, back_btn)
    markup.add(help_btn)
    return markup

def text_file_send_keyboard():
    text_file_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    as_text = types.KeyboardButton("As text")
    as_file = types.KeyboardButton("As '.txt' file📃")
    options_btn = types.KeyboardButton("Back⬇️")
    text_file_markup.add(as_text, as_file)
    text_file_markup.add(options_btn)
    return text_file_markup

def inline_buttons(dir_path: str, call_back: str):
    keyboard = types.InlineKeyboardMarkup()

    if call_back == "month_dir":
        for month_dir in os.listdir(dir_path):
            call_back = f"month_dir:{month_dir}"
            keyboard.add(types.InlineKeyboardButton(f"Show: 📁 {month_dir}", callback_data=call_back))

        return keyboard

    elif call_back == "date_dir":
        with os.scandir(dir_path) as entries:
            for entry in entries:
                if entry.is_dir():
                    call_back = f"date_dir:{entry.name}"
                    keyboard.add(types.InlineKeyboardButton(f"Show me:📁 {entry.name}", callback_data=call_back))

        return keyboard


def send_inline_buttons(dict_files: list[dict]):
    keyboard = types.InlineKeyboardMarkup()
    for data in dict_files:
        f_name = data.get("file_name")
        f_id = data.get("file_id")
        call_back = f"Send me:{f_id}"
        keyboard.add(types.InlineKeyboardButton(f"Send me:📄 {f_name}", callback_data=call_back))

    return keyboard
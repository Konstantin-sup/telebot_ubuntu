"""Well this file was created for a case if the code should to repeat itself,
so i kep my code clean."""

from telebot import types
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

def inline_buttons(dirs_list: list[str]):
    keyboard = types.InlineKeyboardMarkup()
    for data in dirs_list:
        keyboard.add(types.InlineKeyboardButton(f"📁 {data}", callback_data=data))

    return keyboard


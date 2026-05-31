"""Well this file was created for a case if the code should to repeat itself,
so i kep my code clean."""
import os
from telebot import types

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

def del_file_check_keyboard(file_id: str):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("✅ Yes", callback_data=f"ConfirmDelete:{file_id}"),
        types.InlineKeyboardButton("❌ No", callback_data="CancelDelete")
    )

    return keyboard

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

    if call_back in ("month_dir", "month_dir_delete"):
        prefix = call_back
        for month_dir in os.listdir(dir_path):
            keyboard.add(types.InlineKeyboardButton(f"Show: 📁 {month_dir}", callback_data=f"{prefix}:{month_dir}"))

        return keyboard

    elif call_back in ("date_dir", "date_dir_delete"):
        prefix = call_back
        with os.scandir(dir_path) as entries:
            for entry in entries:
                if entry.is_dir():
                    keyboard.add(types.InlineKeyboardButton(f"Show: 📁 {entry.name}", callback_data=f"{prefix}:{entry.name}"))

        return keyboard


def send_inline_buttons(dict_files: list[dict]):
    keyboard = types.InlineKeyboardMarkup()
    seen_groups = set()

    for data in dict_files:
        f_name = data.get("file_name")
        f_id = data.get("file_id")
        media_group_id = data.get("media_group_id")
        media_group_name = data.get("media_group_name")

        if media_group_id:
            if media_group_id in seen_groups:  #1 group 1 name
                continue
            seen_groups.add(media_group_id)
            keyboard.add(types.InlineKeyboardButton(
                f"📸 {media_group_name}",
                callback_data=f"Send group:{media_group_id}"
            ))

        else:
            keyboard.add(types.InlineKeyboardButton(
                f"Send me:📄 {f_name}",
                callback_data=f"Send me:{f_id}"
            ))

    return keyboard

def delete_inline_buttons(dict_files: list[dict]):
    keyboard = types.InlineKeyboardMarkup()
    for data in dict_files:
        f_name = data.get("file_name")
        f_id = data.get("file_id")
        call_back = f"Delete:{f_id}"
        keyboard.add(types.InlineKeyboardButton(f"🗑️ {f_name}", callback_data=call_back))

    return keyboard
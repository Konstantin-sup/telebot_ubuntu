import os
from dotenv import load_dotenv
import telebot
from main_bot_package.telebot_functions import (create_keyboard_panel, inline_buttons,
                                                send_inline_buttons, text_file_send_keyboard, delete_inline_buttons, del_file_check_keyboard)
from main_bot_package.file_date_functions import save_file, show_month_dirs, create_month_path, return_file_as, create_f_name
from db_model.api_functions import create_request

load_dotenv()  #loading .env

bot_TOKEN = os.getenv("BOT_TOKEN")
BOT = telebot.TeleBot(bot_TOKEN)
COMMANDS = ["📁 My files", "📤 Upload", "🗑️ Delete", "❓ Help", "Back⬇️"]
UNSUPPORTED_TYPES = ['sticker', 'location', 'contact', 'poll', 'animation']
SUPPORTED_TYPES = ['document', 'video_note', 'photo', 'video', 'audio', 'voice']

def upload_file_types(message, us_content_type):
    f_types = {
        'document': message.document,
        'video_note': message.video_note,
        'photo': message.photo[-1] if message.photo else None,
        'video': message.video,
        'audio': message.audio,
        'voice': message.voice
               }

    return f_types.get(us_content_type)

def load_content_type(content_type, str_cont_type: str, user_id: str, chat_id: str):
    file_id = content_type.file_id
    file_info = BOT.get_file(file_id)
    downloaded_bytes = BOT.download_file(file_info.file_path)

    if str_cont_type == 'document':
        fl_name = content_type.file_name

    else:
        fl_name = create_f_name(str_cont_type)

    try:
        file_name = save_file(user_id, tele_file_id=file_id, file_bytes=downloaded_bytes,
                            bytes_file_name=fl_name, file_type=str_cont_type)

    except ConnectionError:
        BOT.send_message(chat_id, "🟥 Service is temporarily unavailable, try again later")


    BOT.send_message(chat_id, f"{str_cont_type.capitalize()} was saved successfully✅ as '{file_name}'")


def load_data(message):
    if message.text in COMMANDS:
        reaction_to_button(message)
        return

    try:
        used_space, status = create_request('/get_quota', {"user_id": str(message.from_user.id)})
        user_content_type = message.content_type
        chat_id = message.chat.id
        us_id = message.from_user.id

        if user_content_type in UNSUPPORTED_TYPES:  #currently takes text, documents only.
            BOT.send_message(chat_id, "❌ This type of content is not supported\nTry sending a file, photo, video, audio or text")
            return

        elif message.text:
            text_size = len(message.text.encode("utf-8"))  # weight in bytes

            if used_space + text_size > 250 * 1024 * 1024:
                full_storage(message_chat_id=chat_id, used_space=used_space)
                return

            fl_name = save_file(us_id, file_type="text", text=message.text)
            BOT.send_message(chat_id, f"Text was saved successfully✅ as '{fl_name}'")

        elif user_content_type in SUPPORTED_TYPES:
            file_type = upload_file_types(message, user_content_type)
            file_size = file_type.file_size

            if file_size > 15 * 1024 * 1024:  ## 15 MB
                BOT.send_message(message.chat.id, "File is too heavy, max(15mb)")
                return

            if used_space + file_size > 250 * 1024 * 1024:  #cheking if there place for the next fl
                full_storage(message_chat_id=message.chat.id, used_space=used_space)
                return

            BOT.send_message(message.chat.id, "Got it, may take a lil time⌛ to save it, please wait")
            load_content_type(file_type, str_cont_type=user_content_type, user_id=us_id, chat_id=chat_id)


    except TypeError as e:
        BOT.send_message(message.chat.id, "Unsupported Content, send something else")
        BOT.register_next_step_handler(message, load_data)
        raise e

    # except FileExistsError:
    #     BOT.send_message(
    #         message.chat.id,
    #         "You have already send this file today",
    #         reply_markup=create_keyboard_panel()
    #     )
    #     return

    except Exception as e:
        BOT.send_message(message.chat.id, "🟥 Sorry something went wrong, try again later")
        raise e #will be replaced

def full_storage(message_chat_id: str, used_space: int):
    BOT.send_message(
        message_chat_id,
        f"No more place for this file\n"
        f"Full: {round(used_space / (1024 * 1024), 2)}MB of 250MB\n"
        "Delete files with '🗑️ Delete' to continue"
    )

def send_file_as(response, txt_file_path):
    if response.text == "As text":
        file_text = return_file_as(file_path=txt_file_path, mode="text")
        BOT.send_message(response.chat.id, file_text)
        return

    elif response.text == "As '.txt' file📃":
        txt_file = return_file_as(file_path=txt_file_path, mode="file")
        BOT.send_document(response.chat.id, txt_file, caption="Your .txt file")
        return

    elif response.text == "Back⬇️":
        all_options = create_keyboard_panel()
        BOT.send_message(
            response.chat.id,
            "All options⤵️",
            reply_markup=all_options
        )
        return

    else:
        BOT.send_message(response.chat.id, "No such option")


@BOT.message_handler(commands=['start'])
def start(message):
    BOT.send_message(message.chat.id, "Hello i am bot for working with text, and files\n")
    markup = create_keyboard_panel()

    BOT.send_message(
       message.chat.id,
       "Chose a command ⤵️",
        reply_markup=markup
    )

@BOT.callback_query_handler(func=lambda call: call.data.startswith("month_dir:"))
def handle_month(call):
    BOT.answer_callback_query(call.id)

    month = call.data.split(":")[1]
    month_dir_path = create_month_path(month=month, user_id=call.from_user.id)
    inline = inline_buttons(dir_path=month_dir_path, call_back="date_dir")

    BOT.send_message(
        call.message.chat.id,
        f"Select folder from 📁{month} directory⤵️",
        reply_markup=inline
    )


@BOT.callback_query_handler(func=lambda call: call.data.startswith("date_dir:"))
def handle_date_dir(call):
    BOT.answer_callback_query(call.id)

    date_dir = call.data.split(":")[1]
    user_id = call.from_user.id
    input_json = {"user_id": user_id, "date_dir": date_dir}
    date_dir_files_list, status = create_request(endpoint='/date_dir_files', input_json=input_json)

    date_dir_files_fresh = send_inline_buttons(date_dir_files_list)
    BOT.send_message(
        call.message.chat.id,
        f"Here are your files from 📁{date_dir} directory⤵️",
        reply_markup=date_dir_files_fresh
    )


@BOT.callback_query_handler(func=lambda call: call.data.startswith("Send me:"))
def handle_send_file(call):
    BOT.answer_callback_query(call.id)

    file_id = call.data.split(":")[1]
    user_id = call.from_user.id
    input_json = {"user_id": user_id, "file_id": file_id}
    file_json, status = create_request(endpoint='/file_data', input_json=input_json)
    tele_file_id = file_json.get("tele_file_id")
    file_path = file_json.get("file_path")
    file_type = file_json.get("file_type")

    send_methods = {
        "photo": lambda: BOT.send_photo(call.message.chat.id, tele_file_id, caption="Your photo"),
        "video": lambda: BOT.send_video(call.message.chat.id, tele_file_id, caption="Your video"),
        "video_note": lambda: BOT.send_video_note(call.message.chat.id, tele_file_id),
        "audio": lambda: BOT.send_audio(call.message.chat.id, tele_file_id, caption="Your audio"),
        "voice": lambda: BOT.send_voice(call.message.chat.id, tele_file_id),
        "document": lambda: BOT.send_document(call.message.chat.id, tele_file_id, caption="Your file"),
    }

    if file_type in send_methods:
        send_methods[file_type]()
        return

    #if txt
    send_file_keyboard = text_file_send_keyboard()
    send_file_response = BOT.send_message(
        call.message.chat.id,
        "Send .txt as⤵️",
        reply_markup=send_file_keyboard
    )
    BOT.register_next_step_handler(send_file_response, send_file_as, file_path)

@BOT.callback_query_handler(func=lambda call: call.data.startswith("month_dir_delete:"))
def handle_month_dir_delete(call):
    BOT.answer_callback_query(call.id)
    month = call.data.split(":")[1]
    month_dir_path = create_month_path(month=month, user_id=call.from_user.id)
    inline = inline_buttons(dir_path=month_dir_path, call_back="date_dir_delete")
    BOT.send_message(
        call.message.chat.id,
        f"📁 {month} — select a date to delete🗑️ files from⤵️",
        reply_markup=inline
    )

@BOT.callback_query_handler(func=lambda call: call.data.startswith("date_dir_delete:"))
def handle_date_dir_delete(call):
    BOT.answer_callback_query(call.id)
    date_dir = call.data.split(":")[1]
    user_id = call.from_user.id
    input_json = {"user_id": user_id, "date_dir": date_dir}
    date_dir_files_list, status = create_request(endpoint='/date_dir_files', input_json=input_json)
    inline = delete_inline_buttons(date_dir_files_list)
    BOT.send_message(
        call.message.chat.id,
        f"📁 {date_dir} — select a file to delete🚫️",
        reply_markup=inline
    )

@BOT.callback_query_handler(func=lambda call: call.data.startswith("Delete:"))
def handle_delete_confirm(call):
    BOT.answer_callback_query(call.id)
    file_id = call.data.split(":")[1]
    delete_keyboard = del_file_check_keyboard(file_id=file_id)

    BOT.send_message(
        call.message.chat.id,
        "Are you sure you want to delete this file?",
        reply_markup=delete_keyboard
    )

@BOT.callback_query_handler(func=lambda call: call.data.startswith("ConfirmDelete:"))
def handle_confirm_delete(call):
    BOT.answer_callback_query(call.id)
    file_id = call.data.split(":")[1]
    user_id = call.from_user.id
    status = create_request('/delete_file', {"user_id": user_id, "file_id": file_id})

    if status == 204:
        BOT.send_message(call.message.chat.id, "✅ File deleted successfully")

    else:
        BOT.send_message(call.message.chat.id, "🟥 Something went wrong, try again later")


@BOT.callback_query_handler(func=lambda call: call.data == "CancelDelete")
def handle_cancel_delete(call):
    BOT.answer_callback_query(call.id)
    BOT.send_message(call.message.chat.id, "Deletion cancelled✅")

@BOT.message_handler(func=lambda message: message.text in COMMANDS)
def reaction_to_button(message):
    try:
        if message.text == "📤 Upload":
            BOT.send_message(message.chat.id,
                             "❗Please note that if you send a file with a long name (more than 15 characters), its name will be truncated.")
            BOT.send_message(message.chat.id, "So now send a text or file so i can save it📁")
            BOT.register_next_step_handler(message, load_data)

        elif message.text == "📁 My files":
            months_dir_path = show_month_dirs(message.from_user.id)  #returns path to the months_dirs
            inline = inline_buttons(dir_path=months_dir_path, call_back="month_dir")

            BOT.send_message(
                message.chat.id,
                "Select month folder⤵️",
                reply_markup=inline
            )

        elif message.text == "🗑️ Delete":
            months_dir_path = show_month_dirs(message.from_user.id)
            inline = inline_buttons(dir_path=months_dir_path, call_back="month_dir_delete")
            BOT.send_message(
                message.chat.id,
                "Select a folder to delete from⤵️",
                reply_markup=inline
            )


        elif message.text == "Back⬇️":
            BOT.send_message(
                message.chat.id,
                "All options⤵️",
                reply_markup=create_keyboard_panel()
            )


        elif message.text == "❓ Help":

            used_space, status = create_request('/get_quota', {"user_id": str(message.from_user.id)})

            used_mb = round(used_space / (1024 * 1024), 2)

            BOT.send_message(

                message.chat.id,

                f"❓ Help\n\n"
                f"📁 My files — browse and retrieve your saved files\n\n"
                f"📤 Upload — save content (max 15MB per file):\n"
                f"     • Text\n"
                f"     • Documents\n"
                f"     • Photos\n"
                f"     • Video\n"
                f"     • Video notes (circles)\n"
                f"     • Audio\n"
                f"     • Voice messages\n\n"
                f"🗑️ Delete — delete saved files\n\n"
                f"💾 Storage: {used_mb}MB of 250MB used"

            )

    except FileNotFoundError:
        BOT.send_message(message.chat.id,
                         "You haven't send any file yet")

    except ConnectionError:
        BOT.send_message(message.chat.id, "🟥 Service is temporarily unavailable, try again later")
        return



#filtration
@BOT.message_handler(func=lambda message: True, content_types=['text', 'photo', 'voice', 'document', 'video_note', 'audio'])
def handle_not_supported(message):
    BOT.send_message(
        message.chat.id,
        "No such option, use one of those⤵️",
        reply_markup=create_keyboard_panel()
    )



BOT.polling()



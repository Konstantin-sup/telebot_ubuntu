import os
from dotenv import load_dotenv
import telebot
from main_bot_package.telebot_functions import create_keyboard_panel, inline_buttons, send_inline_buttons, text_file_send_keyboard
from main_bot_package.file_date_functions import save_file, show_month_dirs, create_month_path, return_file_as
from db_model.api_functions import create_request

load_dotenv()  #loading .env

bot_TOKEN = os.getenv("BOT_TOKEN")
BOT = telebot.TeleBot(bot_TOKEN)
COMMANDS = ["📁 My files", "📤 Upload", "🗑️ Delete", "❓ Help", "Back⬇️"]


def load_data(message):
    try:
        if message.content_type in ['voice', 'video_note', 'photo']:  #currently takes text, documents only.
            raise TypeError

        elif message.text:
            fl_name = save_file(message.from_user.id, text=message.text)
            BOT.send_message(message.chat.id, f"Text was saved successfully✅ as '{fl_name}'")

        elif message.document:
            file_size = message.document.file_size

            if file_size > 15 * 1024 * 1024:  ## 15 MB
                BOT.send_message(message.chat.id, "File is too heavy, max(15mb)")
                return

            BOT.send_message(message.chat.id, "Got it, may take a lil time⌛ to save it, please wait")
            file_id = message.document.file_id
            file_info = BOT.get_file(file_id)
            downloaded_bytes = BOT.download_file(file_info.file_path)
            fl_name = save_file(message.from_user.id, tele_file_id=file_id, file_bytes=downloaded_bytes, bytes_file_name=message.document.file_name)
            BOT.send_message(message.chat.id, f"File was saved successfully✅ as '{fl_name}'")

    except TypeError:
        BOT.send_message(message.chat.id, "Currently are only text and files allowed, try again")
        BOT.register_next_step_handler(message, load_data)

    except FileExistsError:
        BOT.send_message(
            message.chat.id,
            "You have already send this file today",
            reply_markup=create_keyboard_panel()
        )

    except Exception as e:
        print(e)  #will be replaced
        BOT.send_message(message.chat.id, "🟥 Sorry something went wrong, try again later")


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
        f"Here is your data from 📁{month} directory⤵️",
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
    file_name = file_json.get("file_name")

    if tele_file_id and not file_name.endswith(".txt"):
        BOT.send_document(call.message.chat.id, tele_file_id, caption="Your file")
        return

    send_file_keyboard = text_file_send_keyboard()
    send_file_response = BOT.send_message(
        call.message.chat.id,
        "Send .txt as⤵️",
        reply_markup=send_file_keyboard
    )
    BOT.register_next_step_handler(send_file_response, send_file_as, file_path)




@BOT.message_handler(func=lambda message: message.text in COMMANDS)
def reaction_to_button(message):
    if message.text == "📤 Upload":
        BOT.send_message(message.chat.id,
                         "❗Please note that if you send a file with a long name (more than 15 characters), its name will be truncated.")
        BOT.send_message(message.chat.id, "So now send a text or file so i can save it📁")
        BOT.register_next_step_handler(message, load_data)

    elif message.text == "📁 My files":
        try:
            months_dir_path = show_month_dirs(message.from_user.id)  #returns path to the months_dirs
            inline = inline_buttons(dir_path=months_dir_path, call_back="month_dir")

            BOT.send_message(
                message.chat.id,
                "Here are yours data⤵️",
                reply_markup=inline
            )

        except FileNotFoundError:
            BOT.send_message(message.chat.id,
                             "You haven't send any file yet")

    elif message.text == "Back⬇️":
        BOT.send_message(
            message.chat.id,
            "All options⤵️",
            reply_markup=create_keyboard_panel()
        )

#filtration👇
@BOT.message_handler(func=lambda message: True, content_types=['text', 'photo', 'voice', 'document', 'video_note'])
def handle_not_supported(message):
    BOT.send_message(
        message.chat.id,
        "No such option, use one of those⤵️",
        reply_markup=create_keyboard_panel()
    )



BOT.polling()



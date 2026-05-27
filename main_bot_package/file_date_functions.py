"""This file was created specially for saving, searching, or deleting files"""
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from db_model.api_functions import create_request


load_dotenv()  #loading .env

months = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}


data_path = os.getenv("PATH_TO_DATA")

def create_f_name(str_content_type: str):
    names_dict = {
        'photo': f"photo_{uuid.uuid4().hex[:5]}.jpg",
        'video_note': f"video_note_{uuid.uuid4().hex[:5]}_.mp4",
        'video': f"video_{uuid.uuid4().hex[:5]}_.mp4",
        'audio': f"audio_{uuid.uuid4().hex[:5]}_.mp3",
        'voice': f"voice_{uuid.uuid4().hex[:5]}.ogg"
    }

    return names_dict.get(str_content_type)

def generate_file_name(file_name: str) -> str:
    f_name, f_format = os.path.splitext(file_name)
    if len(file_name) >= 15:
        return f"{f_name[:10]}_{uuid.uuid4().hex[:5]}{f_format}"

    return f"{f_name}_{uuid.uuid4().hex[:2]}{f_format}"

def get_time_data():  #returns always current time, needs on server where requests 24/7
    now = datetime.now()

    return {
        "day": f"{now.day:02d}.{now.month:02d}",
        "year": str(now.year),
        "month": months[f"{now.month:02d}"],
        "filename": f"{now.day:02d}.{now.month:02d}.txt",  #needs to give a user text name(date) as exampl
        "dir": f'{now.day:02d}.{now.month:02d}'  #dirs also have date names
    }

def create_month_path(month: str, user_id: int) -> str:
    month_path = os.path.join(data_path, str(user_id), get_time_data()["year"], month)
    return month_path

def return_file_as(file_path: str, mode: str):
    if mode == "text":
        with open(file_path, "r", encoding="utf-8") as f_obj:
            return f_obj.read()

    elif mode == "file":
        return open(file_path, "rb")

def txt_file_count(dir_path) -> int:
    return sum(1 for f in os.listdir(dir_path) if f.endswith(".txt"))

def show_month_dirs(user_id) -> str:  #using in Inline_buttons
    if not os.path.exists(os.path.join(data_path, str(user_id))):
        raise FileNotFoundError

    month_dir_path = os.path.join(data_path, str(user_id), get_time_data()["year"])
    return month_dir_path

def save_txt(dir_path, text, time_json: dict):
    file_counted = txt_file_count(dir_path)  # counting files in the dir
    text_file_path = os.path.join(dir_path, f'num({file_counted + 1})_{time_json.get("filename")}')
    write_file(text_file_path, text, encoding="utf-8")
    return text_file_path, f'num({file_counted + 1})_{time_json.get("filename")}' ##file_name

def write_file(file_path, content, mode="w", encoding=None):
    with open(file_path, mode, encoding=encoding) as f_object:
        f_object.write(content)

def create_metadata(user_id: str, file_type: str, file_path: str, month_dir: str, file_name: str, date_dir: str, file_size: int,  tele_file_id= str|None):
    return {
        "user_id": user_id,
        "file_path": file_path,
        "month_dir": month_dir,
        "file_name": file_name,
        "tele_file_id": tele_file_id,
        "date_dir": date_dir,
        "file_size": file_size,
        "file_type": file_type
    }

def save_file(us_id, file_type: str, text=None, file_bytes=None, bytes_file_name=None, tele_file_id=None):
    try:
        create_request('/health', {})

        user_id = us_id  #better to make users_dir with theirs id(they are unique)
        user_dir = os.path.join(data_path, str(user_id))
        time = get_time_data()
        os.makedirs(user_dir, exist_ok=True)  #makes dir for new user if not exists
        os.makedirs(os.path.join(user_dir, time.get("year"), time.get("month")), exist_ok=True) #makes new month dir in users_dir if not exists
        path_current_date_dir = os.path.join(user_dir, time.get("year"), time.get("month"), time.get("dir"))
        os.makedirs(path_current_date_dir, exist_ok=True)

        if text:
            file_path, file_name = save_txt(path_current_date_dir, text, time_json=time)

        elif file_bytes:
            if file_type == "document":
                bytes_file_name = generate_file_name(bytes_file_name)

            file_path = os.path.join(path_current_date_dir, bytes_file_name)
            file_name = bytes_file_name
            write_file(file_path, file_bytes, mode="wb")

        file_size = os.path.getsize(file_path)

        meta_json = create_metadata(
            user_id=str(user_id),
            file_path=file_path,
            month_dir=time.get("month"),
            file_name=file_name,
            tele_file_id=tele_file_id,
            date_dir=time.get("dir"),
            file_size=file_size,
            file_type=file_type
        )

        create_request('/load_metadata', input_json=meta_json)
        create_request('/update_quota', input_json={"user_id": str(us_id), "file_size": file_size})

        return file_name

    except ConnectionError:
        raise ConnectionError


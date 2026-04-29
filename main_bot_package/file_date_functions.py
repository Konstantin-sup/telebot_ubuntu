"""This file was created specially for saving, searching, or deleting files"""
import os
import shutil
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

def get_time_data():  #returns always current time, needs on server where requests 24/7
    now = datetime.now()

    return {
        "day": f"{now.day:02d}.{now.month:02d}",
        "year": str(now.year),
        "month": months[f"{now.month:02d}"],
        "filename": f"{now.day:02d}.{now.month:02d}.txt",  #needs to give a user text name(date) as exampl
        "dir": f'{now.day:02d}.{now.month:02d}'  #dirs also have date names
    }

time = get_time_data()

def txt_file_count(dir_path):
    files_list = os.listdir(dir_path)
    count_txt = lambda lst: sum(1 for i in lst if i.endswith(".txt"))
    return count_txt(files_list)

def save_txt(dir_path, text):
    file_counted = txt_file_count(dir_path)  # counting files in the dir
    text_file_path = os.path.join(dir_path, f'num({file_counted + 1})_{time.get("filename")}')
    write_file(text_file_path, text, encoding="utf-8")
    return text_file_path, f'num({file_counted + 1})_{time.get("filename")}' ##file_name


def write_file(file_path, content, mode="w", encoding=None):
    with open(file_path, mode, encoding=encoding) as f_object:
        f_object.write(content)

def create_metadata(user_id: str, file_path: str, month_dir: str, file_name: str, tele_file_id= str|None):
    return {
        "user_id": user_id,
        "file_path": file_path,
        "month_dir": month_dir,
        "file_name": file_name,
        "tele_file_id": tele_file_id
    }

def save_file(us_id, text=None, file_bytes=None, bytes_file_name=None, tele_file_id=None):
    user_id = us_id  #better to make users_dir with theirs id(they are unique)
    user_dir = os.path.join(data_path, str(user_id))
    os.makedirs(user_dir, exist_ok=True)  #makes dir for new user if not exists
    os.makedirs(os.path.join(user_dir, time.get("year"), time.get("month")), exist_ok=True) #makes new month dir in users_dir if not exists
    path_current_date_dir = os.path.join(user_dir, time.get("year"), time.get("month"), time.get("dir"))
    root_text_f_path = os.path.join(user_dir, time.get("year"), time.get("month"), time.get("filename"))

    if text:  #so now if user sends text to save as more then once we create a dir for that
        if os.path.exists(root_text_f_path):  #checks if file is in root month dir
            os.makedirs(path_current_date_dir, exist_ok=True)
            shutil.move(root_text_f_path, path_current_date_dir)  #moves old file to new dir
            file_path, file_name = save_txt(path_current_date_dir, text)


        elif os.path.exists(path_current_date_dir):  #if date_dir exists, saves file there(if more then 1 file in month_root_dir)
            file_path, file_name = save_txt(path_current_date_dir, text)


        else:
            file_path = root_text_f_path
            write_file(root_text_f_path, text, encoding="utf-8")
            file_name = time.get("filename")


        meta_json = create_metadata(user_id=str(user_id), file_path=file_path, month_dir=time.get("month"), file_name=file_name, tele_file_id=tele_file_id)
        create_request('/load_metadata', input_json=meta_json)


    if file_bytes:
        os.makedirs(path_current_date_dir, exist_ok=True)  #makes date_dir if first file of the day

        if os.path.exists(os.path.join(path_current_date_dir, bytes_file_name)):
            raise FileExistsError

        elif os.path.exists(root_text_f_path):
            shutil.move(root_text_f_path, path_current_date_dir)  #moves .txt in date_dir if .txt in month_root_dir and user sends bytes in same date

        file_path = os.path.join(path_current_date_dir, bytes_file_name)
        write_file(file_path, file_bytes, mode="wb")

        meta_json = create_metadata(user_id=str(user_id), file_path=file_path, month_dir=time.get("month"), file_name=bytes_file_name, tele_file_id=tele_file_id)
        create_request('/load_metadata', input_json=meta_json)







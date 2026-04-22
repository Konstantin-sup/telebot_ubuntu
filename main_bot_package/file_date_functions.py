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
        "month": months[f"{now.month:02d}"],
        "filename": f"{now.day:02d}.{now.month:02d}.txt",  #needs to give a user text name(date) as exampl
        "dir": f'{now.day:02d}.{now.month:02d}'  #dirs also have date names
    }

def file_count(dir_path):
    files_list = os.listdir(dir_path)
    count_txt = lambda lst: sum(1 for i in lst if i.endswith(".txt"))
    return count_txt(files_list)


def save_file(us_id, text=None, file_bytes=None, file_name=None, tele_file_id=None):
    user_id = us_id  #better to make users_dir with theirs id(they are unique)
    time = get_time_data()
    user_dir = os.path.join(data_path, str(user_id))
    os.makedirs(user_dir, exist_ok=True)  #makes dir for new user if not exists
    os.makedirs(os.path.join(user_dir, time.get("month")), exist_ok=True) #makes new month dir in users_dir if not exists
    path_current_date_dir = os.path.join(user_dir, time.get("month"), time.get("dir"))
    new_f_path = os.path.join(user_dir, time.get("month"), time.get("filename"))

    if text:  #so now if user sends text to save as  more then once we create a dir for that
        if os.path.exists(new_f_path):  #checks if file is in root month dir
            os.makedirs(path_current_date_dir, exist_ok=True)
            os.chdir(path_current_date_dir)
            shutil.move(new_f_path, path_current_date_dir)  #moves old file to new dir
            file_counted = file_count(path_current_date_dir)  #counting files in the dir
            file_name = f'num({file_counted+1})_{time.get("filename")}'
            with open(file_name, "w", encoding='utf-8') as f_obj:
                f_obj.write(text)   #writes user_text to the new file and saves it in dir with older ones

            file_path = os.path.abspath(file_name)
            json = {"user_id": str(user_id), "file_id": "3", "file_path": file_path, "tele_file_id": str(tele_file_id)}
            create_request("/load_metadata", input_json=json)

        elif os.path.exists(path_current_date_dir):
            os.chdir(path_current_date_dir)  #if month dir exists saves file there
            file_counted = file_count(path_current_date_dir)  #counting files in the dir
            file_name = f'num({file_counted+1})_{time.get("filename")}'
            with open(file_name, "w", encoding='utf-8') as f_obj:
                f_obj.write(text)

            file_path = os.path.abspath(file_name)
            json = {"user_id": str(user_id), "file_id": "25", "file_path": file_path, "tele_file_id": str(tele_file_id)}
            create_request("/load_metadata", input_json=json)

        else:
            with open(new_f_path, 'w', encoding='utf-8') as f_obj:
                f_obj.write(text)

            file_path = os.path.abspath(new_f_path)
            json = {"user_id": str(user_id), "file_id": "26", "file_path": file_path, "tele_file_id": str(tele_file_id)}
            create_request("/load_metadata", input_json=json)

    if file_bytes:
        os.makedirs(path_current_date_dir, exist_ok=True)  #if first file of the day, making dir

        if os.path.exists(new_f_path):
            shutil.move(new_f_path, path_current_date_dir)  #moves .txt file to the new month dir

        os.chdir(path_current_date_dir)
        with open(file_name, "wb") as f_obj:
            f_obj.write(file_bytes)

        file_path = os.path.abspath(file_name)
        json = {"user_id": str(user_id), "file_id": "29", "file_path": file_path, "tele_file_id": str(tele_file_id)}
        create_request("/load_metadata", input_json=json)


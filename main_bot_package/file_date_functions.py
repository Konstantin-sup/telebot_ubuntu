"""This file was created specially for saving, searching, or deleting files"""
import os
import shutil
from datetime import datetime
from dotenv import load_dotenv

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
    return len(os.listdir(dir_path))


def save_file(us_id, text=None, file_bytes=None, file_name=None):
    user_id = us_id  #better to make users_dir with theirs id(they are unique)
    time = get_time_data()
    user_dir = os.path.join(data_path, str(user_id))
    os.makedirs(user_dir, exist_ok=True)  #makes dir for new user if not exists
    os.makedirs(os.path.join(user_dir, time.get("month")), exist_ok=True) #makes new month dir in users_dir if not exists
    path_current_date_dir = os.path.join(user_dir, time.get("month"), time.get("dir"))

    if text:  #so now if user sends text to save as  more then once we create a dir for that
        new_f_path = os.path.join(user_dir, time.get("month"), time.get("filename"))  #path to the new file

        if os.path.exists(new_f_path):  #checks if file is in root month dir
            os.makedirs(path_current_date_dir, exist_ok=True)
            shutil.move(new_f_path, path_current_date_dir)  #moves old file to new dir
            file_counted = file_count(path_current_date_dir)  #counting files in the dir
            save_path = os.path.join(path_current_date_dir, f'num({file_counted+1})_{time.get("filename")}')
            with open(save_path, "w", encoding='utf-8') as f_obj:
                f_obj.write(text)  #writes user_text to the new file and saves it in dir with older ones

        elif os.path.exists(path_current_date_dir):
            file_counted = file_count(path_current_date_dir)  #counting files in the dir
            save_path = os.path.join(user_dir, time.get("month"), time.get("dir"), f'num({file_counted+1})_{time.get("filename")}')
            with open(save_path, "w", encoding='utf-8') as f_obj:
                f_obj.write(text)

        else:
            with open(new_f_path, 'w', encoding='utf-8') as f_obj:
                f_obj.write(text)

    if file_bytes:
        os.makedirs(path_current_date_dir, exist_ok=True)
        os.chdir(path_current_date_dir)
        with open(file_name, "wb") as f_obj:
            f_obj.write(file_bytes)










    

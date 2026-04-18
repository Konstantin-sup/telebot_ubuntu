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
        "filename": f"{now.day:02d}.{now.month:02d}.txt",
        "dir": f'{now.day:02d}.{now.month:02d}'
    }

def file_count(dir_path):
    return len(os.listdir(dir_path))

def save_text(message, us_id):
    text = message
    user_id = us_id  #better to make users_dir with theirs id(they are unique)
    time = get_time_data()

    user_dir = os.path.join(data_path, str(user_id))
    os.makedirs(user_dir, exist_ok=True)  #makes dir for new user if not exists
    os.makedirs(os.path.join(user_dir, time.get("month")), exist_ok=True) #makes new month dir in users_dir if not exists
    new_f_path = os.path.join(user_dir, time.get("month"), time.get("filename"))  #path to the new file
    path_current_date_dir = os.path.join(user_dir, time.get("month"), time.get("dir"))  #makes path to the dir, if it's needed in cases

    #so now if user sends text to save as .txt more then once we create a dir for that
    if os.path.exists(new_f_path):
        os.makedirs(path_current_date_dir, exist_ok=True)
        shutil.copy2(new_f_path, path_current_date_dir)  #copys old file to new dir, and del old file from root dir
        os.remove(new_f_path)
        file_counted = file_count(path_current_date_dir)

        with open(os.path.join(path_current_date_dir, f'num({file_counted+1})_{time.get("filename")}'), "w", encoding='utf-8') as f_obj:
            f_obj.write(text)

    elif os.path.exists(path_current_date_dir):
        file_counted = file_count(path_current_date_dir)

        with open(os.path.join(user_dir, time.get("month"),
                               time.get("dir"), f'num({file_counted+1})_{time.get("filename")}'), "w", encoding='utf-8') as f_obj:
            f_obj.write(text)

    else:
        with open(new_f_path, 'w', encoding='utf-8') as f_obj:
            f_obj.write(text)











    

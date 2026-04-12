"""This file was created specially for saving, searching, or deleting files"""
import os
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
now = datetime.now()


def save_file(message):
    text = message.text
    user_id = message.from_user.id  #better to make users_dir with theirs id(they are unique)

    user_dir = os.path.join(data_path, str(user_id))
    os.makedirs(user_dir, exist_ok=True)  #makes dir for new user if not exists
    os.makedirs(os.path.join(user_dir, months[f"{now.month:02d}"]), exist_ok=True) #makes new month dir in users_dir if not exists
    new_f_path = os.path.join(user_dir, months[f"{now.month:02d}"], f'{now.day:02d}.{now.month:02d}.txt')  #path to the new file

    with open(new_f_path, 'w', encoding='utf-8') as f_obj:
        f_obj.write(text)











    

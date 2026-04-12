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



    

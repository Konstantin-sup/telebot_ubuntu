from db_model.main_table_model import engine, MainTable
from sqlalchemy.orm import sessionmaker
import requests


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def create_request(endpoint, input_json=None):
    if endpoint == "/load_metadata":
        response = requests.post(f"http://127.0.0.1:8000{endpoint}", json=input_json)
        resp_json = response.json()
        resp_status = response.status_code
        return resp_json, resp_status

def add_metadata(metadata_class):
    index = MainTable(user_id=metadata_class.user_id, file_path=metadata_class.file_path,
                      tele_file_id=metadata_class.tele_file_id,
                      month_dir=metadata_class.month_dir, file_name=metadata_class.file_name)

    session.add(index)
    session.commit()
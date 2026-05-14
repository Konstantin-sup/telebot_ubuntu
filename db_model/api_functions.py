from db_model.main_table_model import engine, MainTable
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import requests


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def create_request(endpoint: str, input_json=dict | None):
    if endpoint == "/load_metadata":
        response = requests.post(f"http://127.0.0.1:8000{endpoint}", json=input_json)
        resp_json = response.json()
        resp_status = response.status_code
        return resp_json, resp_status

    elif endpoint == '/date_dir_files':
        response = requests.get(f"http://127.0.0.1:8000{endpoint}", params=input_json)
        resp_json = response.json()
        resp_status = response.status_code
        return resp_json, resp_status

    elif endpoint == '/file_data':
        response = requests.get(f"http://127.0.0.1:8000{endpoint}", params=input_json)
        resp_json = response.json()
        resp_status = response.status_code
        return resp_json.get("file_data"), resp_status



def add_metadata(metadata_class):
    index = MainTable(user_id=metadata_class.user_id, file_path=metadata_class.file_path,
                      tele_file_id=metadata_class.tele_file_id, date_dir=metadata_class.date_dir,
                      month_dir=metadata_class.month_dir, file_name=metadata_class.file_name)

    session.add(index)
    session.commit()
    session.refresh(index)

    return index.file_id, index.file_path


def get_date_dir_files(user_id: str, date_dir: str):
    result = session.execute(
        select(MainTable)
        .where(
            MainTable.user_id == user_id,
            MainTable.date_dir == date_dir
        )
        .order_by(MainTable.date_creation.asc())
    ).scalars().all()

    return result


def get_file_data(user_id: str, file_id: int):
    result = session.execute(
        select(MainTable)
        .where(
            MainTable.user_id == user_id,
            MainTable.file_id == file_id
        )
    ).scalars().first()

    return result

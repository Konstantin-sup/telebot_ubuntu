from db_model.main_table_model import engine, MainTable
from db_model.user_quota_model import UserQuota
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from datetime import datetime
import requests


SessionLocal = sessionmaker(bind=engine)

def row_to_dict(row, long_list: bool) -> dict | list[dict]:  #long_list = len(long_list)>1
    if not long_list:
        return {
            c.name: getattr(row, c.name).isoformat() if isinstance(getattr(row, c.name), datetime) else getattr(row, c.name)
            for c in row.__table__.columns
        }

    return [
        {
            c.name: getattr(line, c.name).isoformat() if isinstance(getattr(line, c.name), datetime) else getattr(line,
                                                                                                                  c.name)
            for c in line.__table__.columns
        }
        for line in row
        ]

def create_request(endpoint: str, input_json=dict | None):
    try:
        if endpoint == "/load_metadata":
            response = requests.post(f"http://127.0.0.1:8000{endpoint}", json=input_json)
            resp_json = response.json()
            resp_status = response.status_code
            return resp_json, resp_status

        elif endpoint == '/date_dir_files':
            response = requests.get(f"http://127.0.0.1:8000{endpoint}", params=input_json)
            resp_json = response.json()
            resp_status = response.status_code
            return resp_json.get("date_dir_files"), resp_status

        elif endpoint == '/file_data':
            response = requests.get(f"http://127.0.0.1:8000{endpoint}", params=input_json)
            resp_json = response.json()
            resp_status = response.status_code
            return resp_json.get("file_data"), resp_status

        elif endpoint == '/get_quota':
            response = requests.get(f"http://127.0.0.1:8000{endpoint}", params=input_json)
            return response.json().get("used_space"), response.status_code

        elif endpoint == '/update_quota':
            response = requests.patch(f"http://127.0.0.1:8000{endpoint}", params=input_json)
            return response.json(), response.status_code

        elif endpoint == '/delete_file':
            response = requests.delete(f"http://127.0.0.1:8000{endpoint}", params=input_json)
            return response.status_code

    except requests.exceptions.ConnectionError:
        raise ConnectionError("FastAPI is unavailable")


def add_metadata(metadata_class):
    with SessionLocal() as session:
        index = MainTable(user_id=metadata_class.user_id, file_path=metadata_class.file_path,
                          tele_file_id=metadata_class.tele_file_id, date_dir=metadata_class.date_dir,
                          month_dir=metadata_class.month_dir, file_name=metadata_class.file_name,
                          file_size=metadata_class.file_size, file_type=metadata_class.file_type)


        session.add(index)
        session.commit()
        session.refresh(index)

        return index.file_id, index.file_path


def get_date_dir_files(user_id: str, date_dir: str):
    with SessionLocal() as session:
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
    with SessionLocal() as session:
        result = session.execute(
            select(MainTable)
            .where(
                MainTable.user_id == user_id,
                MainTable.file_id == file_id
            )
        ).scalars().first()

        return result


def get_user_quota(user_id: str):
    with SessionLocal() as session:
        return session.execute(
            select(UserQuota).where(UserQuota.user_id == user_id)
        ).scalars().first()


def update_user_quota(user_id: str, file_size: int):
    with SessionLocal() as session:
        quota = get_user_quota(user_id)

        if quota is None:  #if users first file
            new_quota = UserQuota(user_id=user_id, used_space=file_size)
            session.add(new_quota)
        else:
            quota.used_space += file_size  #file_size could be also negative

        session.commit()


def remove_file(user_id: str, file_id: int):
    with SessionLocal() as session:
        file = get_file_data(user_id=user_id, file_id=file_id)  #class from main_table

        if file is None:
            return None

        file_path = file.file_path
        file_size = file.file_size

        # updating quota if user del file            |here is minus
        update_user_quota(user_id=user_id, file_size=-file_size)

        session.delete(file)  # also deleting metadata from main_table
        session.commit()


    if os.path.exists(file_path):
        date_dir = os.path.dirname(file_path)  # date_dir
        month_dir = os.path.dirname(date_dir)  # month_dir
        year_dir = os.path.dirname(month_dir)  # year_dir

        os.remove(file_path)

        if len(os.listdir(date_dir)) == 0:
            os.rmdir(date_dir)

        if len(os.listdir(month_dir)) == 0:
            os.rmdir(month_dir)

        if len(os.listdir(year_dir)) == 0:
            os.rmdir(year_dir)

    return True
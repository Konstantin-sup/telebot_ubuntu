from db_model.main_table_model import MainTable
from db_model.user_quota_model import UserQuota
import os
from sqlalchemy import select
from datetime import datetime
import requests

API_URL = os.getenv("API_URL")

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
            response = requests.post(f"{API_URL}{endpoint}", json=input_json)
            resp_json = response.json()
            resp_status = response.status_code
            return resp_json, resp_status

        elif endpoint == "/health":
            response = requests.get(f"{API_URL}{endpoint}")
            resp_status = response.status_code
            return resp_status

        elif endpoint == '/date_dir_files':
            response = requests.get(f"{API_URL}{endpoint}", params=input_json)
            resp_json = response.json()
            resp_status = response.status_code
            return resp_json.get("date_dir_files"), resp_status

        elif endpoint == '/file_data':
            response = requests.get(f"{API_URL}{endpoint}", params=input_json)
            resp_json = response.json()
            resp_status = response.status_code
            return resp_json.get("file_data"), resp_status

        elif endpoint == '/get_quota':
            response = requests.get(f"{API_URL}{endpoint}", params=input_json)
            return response.json().get("used_space"), response.status_code

        elif endpoint == '/update_quota':
            response = requests.patch(f"{API_URL}{endpoint}", params=input_json)
            return response.json(), response.status_code

        elif endpoint == '/delete_file':
            response = requests.delete(f"{API_URL}{endpoint}", params=input_json)
            return response.status_code

        elif endpoint == '/group_files':
            response = requests.get(f"{API_URL}{endpoint}", params=input_json)
            return response.json().get("group_files"), response.status_code

        elif endpoint == '/delete_group':
            response = requests.delete(f"{API_URL}{endpoint}", params=input_json)
            return response.status_code

    except requests.exceptions.ConnectionError:
        raise ConnectionError("FastAPI is unavailable")


def add_metadata(metadata_class, session):
    index = MainTable(user_id=metadata_class.user_id, file_path=metadata_class.file_path,
                      tele_file_id=metadata_class.tele_file_id, date_dir=metadata_class.date_dir,
                      month_dir=metadata_class.month_dir, file_name=metadata_class.file_name,
                      file_size=metadata_class.file_size, file_type=metadata_class.file_type,
                      media_group_id=metadata_class.media_group_id,media_group_name=metadata_class.media_group_name
                      )

    session.add(index)
    session.commit()
    session.refresh(index)
    return index.file_id, index.file_path


def get_date_dir_files(user_id: str, date_dir: str, session):
    return session.execute(
        select(MainTable)
        .where(MainTable.user_id == user_id, MainTable.date_dir == date_dir)
        .order_by(MainTable.date_creation.asc())
    ).scalars().all()


def get_file_data(user_id: str, file_id: int, session):
    return session.execute(
        select(MainTable)
        .where(MainTable.user_id == user_id, MainTable.file_id == file_id)
    ).scalars().first()


def get_user_quota(user_id: str, session):
    return session.execute(
        select(UserQuota).where(UserQuota.user_id == user_id)
    ).scalars().first()


def update_user_quota(user_id: str, file_size: int, session):
    quota = get_user_quota(user_id=user_id, session=session)
    if quota is None:
        session.add(UserQuota(user_id=user_id, used_space=file_size))
    else:
        quota.used_space += file_size
    session.commit()


def remove_file(user_id: str, file_id: int, session):
    file = get_file_data(user_id=user_id, file_id=file_id, session=session)

    if file is None:
        return None

    file_path = file.file_path
    file_size = file.file_size

    update_user_quota(user_id=user_id, file_size=-file_size, session=session)
    session.delete(file)
    session.commit()

    if os.path.exists(file_path):
        date_dir = os.path.dirname(file_path)
        month_dir = os.path.dirname(date_dir)
        year_dir = os.path.dirname(month_dir)

        os.remove(file_path)

        if len(os.listdir(date_dir)) == 0:
            os.rmdir(date_dir)
        if len(os.listdir(month_dir)) == 0:
            os.rmdir(month_dir)
        if len(os.listdir(year_dir)) == 0:
            os.rmdir(year_dir)

    return True

def get_group_files(user_id: str, media_group_id: str, session):
    return session.execute(
        select(MainTable)
        .where(
            MainTable.user_id == user_id,
            MainTable.media_group_id == media_group_id
        )
    ).scalars().all()

def remove_group(user_id: str, media_group_id: str, session):
    files = get_group_files(user_id=user_id, media_group_id=media_group_id, session=session)

    if not files:
        return None

    total_size = sum(file.file_size for file in files)
    file_paths = [file.file_path for file in files]

    update_user_quota(user_id=user_id, file_size=-total_size, session=session)

    for file in files:
        session.delete(file)
    session.commit()

    for file_path in file_paths:
        if os.path.exists(file_path):
            date_dir = os.path.dirname(file_path)
            month_dir = os.path.dirname(date_dir)
            year_dir = os.path.dirname(month_dir)

            os.remove(file_path)

            if len(os.listdir(date_dir)) == 0:
                os.rmdir(date_dir)
            if len(os.listdir(month_dir)) == 0:
                os.rmdir(month_dir)
            if len(os.listdir(year_dir)) == 0:
                os.rmdir(year_dir)

    return True
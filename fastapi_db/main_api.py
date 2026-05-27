from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.responses import Response
from db_model.api_functions import (add_metadata, get_date_dir_files, get_file_data,
                                    row_to_dict, get_user_quota, update_user_quota, remove_file)
app = FastAPI()

class Metadata(BaseModel):
    user_id: str
    file_path: str
    tele_file_id: str | None = None  #user can also send text(only when user sends doc)
    month_dir: str
    file_name: str
    date_dir: str
    file_size: int
    file_type: str


@app.get('/health')
def health():
    return JSONResponse(status_code=200, content={"ok": True})

@app.post('/load_metadata')
def load_file_data(file_data: Metadata):
    file_id, file_path = add_metadata(file_data)

    return JSONResponse(status_code=201, content={"file_id": file_id, "file_path": file_path})


@app.get('/date_dir_files')
def select_files(user_id: str, date_dir: str):
    result = get_date_dir_files(user_id=user_id, date_dir=date_dir)

    return JSONResponse(status_code=200, content={"date_dir_files": row_to_dict(result, long_list=True)})


@app.get('/file_data')
def send_file_data(user_id: str, file_id: int):
    file_data = get_file_data(user_id=user_id, file_id=file_id)

    return JSONResponse(status_code=200, content={"file_data": row_to_dict(file_data, long_list=False)})


@app.get('/get_quota')
def get_quota(user_id: str):
    quota = get_user_quota(user_id=user_id)

    if quota is None:  #if new user
        return JSONResponse(status_code=200, content={"used_space": 0})

    return JSONResponse(status_code=200, content={"used_space": quota.used_space})


@app.patch('/update_quota')
def update_quota(user_id: str, file_size: int):
    update_user_quota(user_id=user_id, file_size=file_size)
    return JSONResponse(status_code=200, content={"ok": True})


@app.delete('/delete_file')
def delete_file(user_id: str, file_id: int):
    result = remove_file(user_id=user_id, file_id=file_id)

    if not result:
        return JSONResponse(status_code=404, content={"error": "file not found"})

    return Response(status_code=204) #idk why but content is required even if 204



#uvicorn fastapi_db.main_api:app --reload

#curl "http://localhost:8000/file_data?user_id="5304343110"&file_id=21

#curl "http://localhost:8000/date_dir_files?user_id="5304343110"&date_dir=02.05"
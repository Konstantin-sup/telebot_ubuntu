from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db_model.api_functions import add_metadata, get_date_dir_files, get_file_data, row_to_dict
app = FastAPI()

class Metadata(BaseModel):
    user_id: str
    file_path: str
    tele_file_id: str | None = None  #user can also send text(only when user sends doc)
    month_dir: str
    file_name: str
    date_dir: str

# class SelectFiles(BaseModel):
#     user_id: str
#     date_dir: str


@app.post('/load_metadata')
def load_file_data(file_data: Metadata):
    file_id, file_path = add_metadata(file_data)

    return JSONResponse(status_code=200, content={"file_id": file_id, "file_path": file_path})



@app.get('/date_dir_files')
def select_files(user_id: str, date_dir: str):

    result = get_date_dir_files(user_id=user_id, date_dir=date_dir)
    return result  #JSONRESPONSE later


@app.get('/file_data')
def send_file_data(user_id: str, file_id: int):
    file_data = get_file_data(user_id=user_id, file_id=file_id)

    return JSONResponse(status_code=200, content={"file_data": row_to_dict(file_data)})

#uvicorn fastapi_db.main_api:app --reload



#curl "http://localhost:8000/file_data?user_id="5304343110"&file_id=21
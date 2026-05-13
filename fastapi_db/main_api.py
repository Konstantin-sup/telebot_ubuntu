from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db_model.api_functions import add_metadata, get_date_dir_files
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

#uvicorn fastapi_db.main_api:app --reload




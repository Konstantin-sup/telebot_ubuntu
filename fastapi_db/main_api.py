from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db_model.api_functions import add_metadata
app = FastAPI()

class Metadata(BaseModel):
    user_id: str
    file_path: str
    tele_file_id: str | None = None  #user can also send text(only when user sends doc)
    month_dir: str
    file_name: str


@app.post('/load_metadata')
def load_file_data(file_data: Metadata):
    add_metadata(file_data)

    return JSONResponse(status_code=200, content={"message": "Metadata was saved successfully"})



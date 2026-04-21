from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Metadata(BaseModel):
    user_id: str
    file_id: str
    file_path: str
    tele_file_id: str


@app.post('/load_metadata')
def load_file_data(file_data: Metadata)

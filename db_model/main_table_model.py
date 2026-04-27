import os
from db_model.declarative_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  #loading .env

db_url = os.getenv("DB_URL")
engine = create_engine(db_url, echo=True)

class MainTable(Base):
    __tablename__ = "main_table"

    user_id: Mapped[str] = mapped_column(VARCHAR(60))
    file_id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    file_path: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    tele_file_id: Mapped [str] = mapped_column(VARCHAR(255))



    
import os
from db_model.declarative_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, create_engine, DateTime
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  #loading .env

db_url = os.getenv("DB_URL")
engine = create_engine(db_url, echo=True)

class MainTable(Base):
    __tablename__ = "main_table"

    user_id: Mapped[str] = mapped_column(VARCHAR(60))
    file_id: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    file_path: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    month_dir: Mapped[str] = mapped_column(VARCHAR(60))
    tele_file_id: Mapped [str] = mapped_column(VARCHAR(255))



    
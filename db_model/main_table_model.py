import os
from db_model.declarative_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, create_engine, DateTime, BIGINT
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  #loading .env

db_url = os.getenv("DB_URL")
engine = create_engine(db_url, echo=True)

class MainTable(Base):
    __tablename__ = "main_table"

    user_id: Mapped[str] = mapped_column(VARCHAR(60))
    file_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    file_name: Mapped[str] = mapped_column(VARCHAR(60), unique=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    month_dir: Mapped[str] = mapped_column(VARCHAR(60))
    tele_file_id: Mapped [str] = mapped_column(VARCHAR(255))



    
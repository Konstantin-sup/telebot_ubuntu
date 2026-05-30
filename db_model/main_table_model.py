
from db_model.declarative_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, DateTime, BIGINT
from datetime import datetime


class MainTable(Base):
    __tablename__ = "main_table"

    user_id: Mapped[str] = mapped_column(VARCHAR(60))
    file_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    file_name: Mapped[str] = mapped_column(VARCHAR(60), unique=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    month_dir: Mapped[str] = mapped_column(VARCHAR(60))
    tele_file_id: Mapped [str] = mapped_column(VARCHAR(255), nullable=True)
    date_dir: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=False)
    file_size: Mapped[int] = mapped_column(BIGINT, nullable=False)
    file_type: Mapped[str] = mapped_column(VARCHAR(100), unique=False, nullable=False, server_default='document')  #server_default needed so db doesn't fall before tests
    media_group_id: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    media_group_name: Mapped[str] = mapped_column(VARCHAR(125), nullable=True)
    
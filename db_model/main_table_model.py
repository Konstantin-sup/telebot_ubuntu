from db_model.declarative_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Integer

class MainTable(Base):
    __tablename__ = "main_table"

    user_id: Mapped[str] = mapped_column(VARCHAR(60), primary_key=True)
    file_id: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    file_path: Mapped[str] = mapped_column(VARCHAR(255))
    tele_file_id: Mapped [str] = mapped_column(VARCHAR(255))



    
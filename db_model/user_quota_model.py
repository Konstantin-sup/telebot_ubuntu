from db_model.declarative_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, BIGINT


class UserQuota(Base):
    __tablename__ = "user_quota"

    user_id: Mapped[str] = mapped_column(VARCHAR(60), primary_key=True)
    used_space: Mapped[int] = mapped_column(BIGINT, default=0)  #in bytes

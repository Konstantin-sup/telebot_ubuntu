import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url, echo=True, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)




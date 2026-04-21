from db_model.main_table_model import engine, MainTable
from sqlalchemy.orm import sessionmaker


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def add_metadata(metadata_class):
    index = MainTable(user_id=metadata_class.user_id, file_id=metadata_class.file_id,
                      file_path=metadata_class.file_path, tele_file_id=metadata_class.tele_file_id)

    session.add(index)
    session.commit()
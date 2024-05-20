from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)

session = Session(engine)
    
def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()



from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = config('DB_URL')
print("-------------------------------")
print(DB_URL)
print("-------------------------------")
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

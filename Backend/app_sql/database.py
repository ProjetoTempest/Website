from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


from sqlmodel import Field, SQLModel, Relationship, create_engine, Session, select, String
from typing import List, Optional


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)

# session = Session(engine)

# cargo1 = Cargo(name="Administrador", description="Acesso total ao sistema")
# user1 = User(name="Administrador", email="email", photo="fto", description='despro', password="123", cargotes=1)

# session.add(user1)
# session.add(cargo1)

# session.commit()

# a = UserBase(session.refresh(user1))
# print(a)

session = Session(engine)
    
    # statement = select(User).where(User.id == 1)
    # results = session.exec(statement).first()
    # # print(results)

    # user_data = results.__fields__
    # user_data = dict(user_data)
    # user_data.pop('cargotes')
    # user_data.pop("password")

    # # a = UserBase(**user_data)
    # # print(a)
    # print(user_data)

# Dependency
def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()
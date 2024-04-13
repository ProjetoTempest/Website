# from sqlalchemy.orm import Session
from sqlmodel import Session, select

from . import models, schemas


def get_user(db: Session, user_id: int):
    # return db.query(models.User).filter(models.User.id == user_id).first()
    # return db.query(schemas.User).filter(models.User.id == user_id).first()
    query = select(schemas.User).where(schemas.User.id == user_id)
    user_db = db.exec(query).first()

    user_db = user_db.model_dump()

    user_db.pop('password')
    user_db.pop('cargotes')

    return user_db


def get_user_by_email(db: Session, email: str):
    query = select(schemas.User).where(schemas.User.email == email)
    return db.exec(query).first()
    # return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    # fake_hashed_password = user.password + "notreallyhashed"
    db_user = schemas.User(name=user.name, email=user.email, cargotes=user.cargotes, photo=user.photo, description=user.description, password=user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    a=db_user.model_dump()
    print(type(a))
    a.pop('password')
    # a.pop('email')
    a.pop('cargotes')

    return a


    # print(user.model_dump())
    # # Crie o objeto User com os dados fornecidos
    # db_user = models.User(user.model_dump())
    # # print(db_user)

    # # Adicione o usuário ao banco de dados
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)

    # # Converta o objeto db_user em um dicionário
    # # user_dict = db_user.dict()

    # # Remova os campos 'password' e 'email' do dicionário
    # # user_dict.pop('password', None)
    # # user_dict.pop('email', None)

    # # Crie um objeto de esquema User para retornar
    # return db_user








    # db_user = models.User(name=user.name, cpf=user.cpf, email=user.email, cargo=user.cargo, photo=user.photo, description=user.description, password=user.password)

    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ProductsCreate, user_id: int):
#     db_item = models.Products(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
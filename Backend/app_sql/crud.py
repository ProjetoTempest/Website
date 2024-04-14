# from sqlalchemy.orm import Session
from sqlmodel import Session, select
from . import schemas


def get_user(db: Session, user_id: int):
    query = select(schemas.User).where(schemas.User.id == user_id)
    user_db = db.exec(query).first()

    user_db = user_db.model_dump()

    user_db.pop('password')
    user_db.pop('cargotes')

    return user_db


def get_user_by_email(db: Session, email: str):
    query = select(schemas.User).where(schemas.User.email == email)
    return db.exec(query).first()

def get_user_by_email_password(db: Session, email: str, password: str):
    user_db = get_user_by_email(db, email)

    if user_db.password == password:
        user_db = user_db.model_dump()
        return user_db
    return None

def get_users(db: Session, skip: int = 0, limit: int = 100):
    query = select(schemas.User).offset(skip).limit(limit)
    users_db = db.exec(query)
    return users_db


def create_user(db: Session, user: schemas.User):
    db_user = schemas.User(name=user.name, email=user.email, cargotes=user.cargotes, photo=user.photo, description=user.description, password=user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


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
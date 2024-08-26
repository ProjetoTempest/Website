from sqlalchemy.orm import Session
from .. import schemas, models

import json


def get_user(db: Session, user_id: int):
    """
    Retorna um usuário com base no ID fornecido.

    Args:
        db (Session): A sessão do banco de dados.
        user_id (int): O ID do usuário.

    Returns:
        models.User | None: O usuário encontrado ou None se nenhum usuário corresponder ao ID fornecido.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Retorna um usuário com o e-mail fornecido.

    Args:
        db (Session): A sessão do banco de dados.
        email (str): O e-mail do usuário.

    Returns:
        models.User: O usuário encontrado, ou None se não encontrado.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_password(db: Session, email: str, password: str):
    """
    Retorna um usuário com base no email e senha fornecidos.

    Args:
        db (Session): A sessão do banco de dados.
        email (str): O email do usuário.
        password (str): A senha do usuário.

    Returns:
        models.User | None: O usuário encontrado ou None se nenhum usuário corresponder aos critérios.
    """
    return db.query(models.User).filter(models.User.email == email, models.User.password == password).first()

def get_users(db: Session):
    """
    Retorna todos os usuários do banco de dados.

    Args:
        db (Session): A sessão do banco de dados.

    Returns:
        list[models.User]: Uma lista de todos os usuários.
    """
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Cria um novo usuário com base nos dados fornecidos.

    Args:
        db (Session): A sessão do banco de dados.
        user (schemas.UserCreate): Os dados do usuário a ser criado.

    Returns:
        models.User: O usuário criado.
    """

    user = user.model_dump()
    db_user = models.User(**user)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Colocar senha para verificação
def update_email_user(db: Session, new_email:str, old_email):
    """
    Atualiza o e-mail de um usuário.

    Args:
        db (Session): A sessão do banco de dados.
        new_email (str): O novo e-mail.
        old_email (str): O e-mail antigo.

    Returns:
        models.User: O usuário atualizado.
    """
    user = get_user_by_email(db=db, email=old_email)

    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
        return user
    return None

# def update_all_infos_user(db: Session, user: schemas.UserCreate):
#     pass

def update_user_fields(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    """
    Atualiza os dados de um usuário.

    Args:
        db (Session): A sessão do banco de dados.
        db_user (models.User): O objeto de usuário existente.
        user_update (schemas.UserUpdate): Os dados atualizados do usuário.

    Returns:
        models.User: O usuário atualizado.
    """

    update_data = user_update.model_dump(exclude_unset=True)
    print(update_data)

    for key, value in update_data.items():
        match key:
            case "name":
                db_user.name = value
            case "email":
                db_user.email = value
            case "role_id":
                db_user.role_id = value
            case "photo":
                db_user.photo = value
            case "description":
                db_user.description = value
            case "password":
                db_user.password = value

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_email_password(db: Session, email: str, password: str):
    """
    Deleta um usuário com base no email e senha fornecidos.

    Args:
        db (Session): A sessão do banco de dados.
        email (str): O email do usuário a ser deletado.
        password (str): A senha do usuário a ser deletado.

    Returns:
        int: O número de registros deletados. Retorna 0 se nenhum registro foi encontrado.
    """
    flag = db.query(models.User).filter(models.User.email == email, models.User.password == password).delete()
    db.commit()
    return flag


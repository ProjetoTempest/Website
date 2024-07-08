from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, HTTPException
from typing import Annotated, List

from fastapi.responses import FileResponse
from pathlib import Path
from typing import Annotated
from fastapi import File, Form, UploadFile

import os
import shutil
import json


from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas
from ..controllers import user_controller

routerUser = APIRouter(prefix="/users")

def safe_file_to_server(uploaded_file, name_user):
    path = "/home/will/Documentos/project_tempest/Website/Backend/imagens/"
    if not os.path.exists(path):
        os.makedirs(path)

    extension = os.path.splitext(uploaded_file.filename) [-1]
    temp_file_name = os.path.join(path, name_user + extension)

    with open(temp_file_name, "wb") as buffer:
        shutil.copyfileobj (uploaded_file.file, buffer)
    return temp_file_name

"""
    Rota para criar um user

    Args:
        user (models.UserCreate): Dados do user.
        db (Session): Cria e gerencia transações do banco de dados.

    Returns:
        models.UserBase: A soma de a e b.
"""
@routerUser.post("/", response_model= schemas.UserBase)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo usuário na aplicação.

    Este endpoint recebe os dados do usuário e cria um novo registro no banco de dados.
    Se o email já estiver registrado, retorna um erro 400.

    Args:
        user (models.UserCreate): Um objeto que contém os dados do usuário a ser criado.
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        models.UserBase: Um objeto que representa o usuário criado, sem a senha.

    Raises:
        HTTPException: Se o email já estiver registrado, retorna uma exceção HTTP 400.
    """

    db_user = user_controller.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_controller.create_user(db=db, user=user) 

@routerUser.get("/{user_id}", response_model= schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtém um usuário pelo ID.

    Este endpoint recebe um ID de usuário e retorna os detalhes do usuário correspondente.
    Se o usuário não for encontrado, retorna um erro 404.

    Args:
        user_id (int): O ID do usuário a ser recuperado.
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        schemas.UserBase: Um objeto que representa os detalhes do usuário.

    Raises:
        HTTPException: Se o usuário não for encontrado, retorna uma exceção HTTP 404.
    """
    db_user = user_controller.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@routerUser.get("/login/{email}/{senha}", response_model=schemas.UserBase)
def login_user(email: str, senha: str, db: Session = Depends(get_db)):
    """
    Autentica um usuário pelo email e senha.

    Este endpoint recebe um email e uma senha e retorna os detalhes do usuário correspondente,
    caso a autenticação seja bem-sucedida. Se o usuário não for encontrado, retorna um erro 404.

    Args:
        email (str): O email do usuário a ser autenticado.
        senha (str): A senha do usuário a ser autenticado.
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        schemas.UserBase: Um objeto que representa os detalhes do usuário autenticado.

    Raises:
        HTTPException: Se o usuário não for encontrado, retorna uma exceção HTTP 404.
    """
    db_user = user_controller.get_user_by_email_password(db, email=email, password=senha)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@routerUser.get("/", response_model=list[schemas.UserBasePass])
def read_users(db: Session = Depends(get_db)):
    """
    Obtém todos os usuários.

    Este endpoint retorna uma lista com todos os usuários registrados no banco de dados.

    Args:
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        list[schemas.UserBase]: Uma lista de objetos que representam os usuários registrados.
    """
    users = user_controller.get_users(db)
    return users

@routerUser.put("/upadate_email/{new_email}/{old_email}", response_model= schemas.UserBase)
def update_email(new_email: str, old_email: str, db: Session = Depends(get_db)):
    """
    Atualiza o e-mail de um usuário.

    Este endpoint atualiza o e-mail de um usuário existente. Se o usuário com o e-mail antigo não for encontrado, retorna um erro 404.

    Args:
        old_email (str): O e-mail antigo do usuário.
        new_email (str): O novo e-mail do usuário.
        db (Session): A sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        schemas.UserBase: Os dados do usuário atualizado.
    """

    updated_user = user_controller.update_email_user(db=db, new_email=new_email, old_email=old_email)

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@routerUser.put("/update_user/{user_id}", response_model=schemas.UserBase)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um usuário.

    Este endpoint atualiza os dados de um usuário existente. Apenas os campos fornecidos (não `None`)
    serão atualizados. Se o usuário não for encontrado, retorna um erro 404.

    Args:
        user_id (int): O ID do usuário a ser atualizado.
        user_update (schemas.UserUpdate): Os dados atualizados do usuário.
        db (Session): A sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        schemas.UserBase: Os dados do usuário atualizado.
    """
    db_user = user_controller.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    print(db_user)

    updated_user = user_controller.update_user_fields(db=db, db_user=db_user, user_update=user_update)

    return updated_user

@routerUser.delete("/delete/{email}/{password}")
def delete_user(email: str, password: str, db: Session = Depends(get_db)):
    """
    Deleta um usuário com base no email e senha fornecidos.

    Args:
        email (str): O email do usuário a ser deletado.
        password (str): A senha do usuário a ser deletado.
        db (Session): A sessão do banco de dados, fornecida automaticamente pelo FastAPI.

    Raises:
        HTTPException: Se o usuário não for encontrado ou a senha estiver incorreta, retorna uma exceção HTTP 400 com a mensagem "User not found or incorrect password".

    Returns:
        dict: Um dicionário com uma mensagem de sucesso e o status HTTP 200.
    """
    deleted_count = user_controller.delete_user_by_email_password(db=db, email=email, password=password)

    if deleted_count == 0:
        raise HTTPException(status_code=400, detail="User not found or incorrect password")
    return {"message": "User deleted successfully", "status": 200}


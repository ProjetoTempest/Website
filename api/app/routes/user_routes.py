from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Any, Dict

from app.db.connection import get_db
from app.schemas.user import UserRequest, UserResponse, UserUpdate
from app.use_cases.user import UserCases


router = APIRouter(prefix="/users")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserRequest,
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
    
    return UserCases(db_session=db).add(user)

@router.get("/{user_id}", response_model= UserResponse)
def read_user(user_id: str, db: Session = Depends(get_db)):
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
    return UserCases(db_session=db).get(user_id)



# @routerUser.get("/login/{email}/{senha}", response_model=schemas.UserBase)
# def login_user(email: str, senha: str, db: Session = Depends(get_db)):
#     """
#     Autentica um usuário pelo email e senha.

#     Este endpoint recebe um email e uma senha e retorna os detalhes do usuário correspondente,
#     caso a autenticação seja bem-sucedida. Se o usuário não for encontrado, retorna um erro 404.

#     Args:
#         email (str): O email do usuário a ser autenticado.
#         senha (str): A senha do usuário a ser autenticado.
#         db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

#     Returns:
#         schemas.UserBase: Um objeto que representa os detalhes do usuário autenticado.

#     Raises:
#         HTTPException: Se o usuário não for encontrado, retorna uma exceção HTTP 404.
#     """
#     db_user = user_controller.get_user_by_email_password(db, email=email, password=senha)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@router.get("/all/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    """
    Obtém todos os usuários.

    Este endpoint retorna uma lista com todos os usuários registrados no banco de dados.

    Args:
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        list[schemas.UserBase]: Uma lista de objetos que representam os usuários registrados.
    """

    return UserCases(db_session=db).get_all()


@router.put("/update/", status_code=status.HTTP_200_OK)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db)):
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
    
    return UserCases(db_session=db).update(user_update)

# @router.delete("/delete/{email}/{password}")
@router.delete("/delete/")
def delete_user(id: str, db: Session = Depends(get_db)):
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

    return UserCases(db_session=db).delete(user_id=id)


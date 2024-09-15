from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.use_cases.user import UserCases as User
from app.schemas.login import Request
from app.schemas.user import UserResponseLogin

router = APIRouter(prefix="/login")




@router.post("/", status_code=200)
def login_user(token: Request, db: Session = Depends(get_db)):
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



    db_user = User(db).login(token)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
    # return {"msg": "Usuário cadastrado com sucesso"}
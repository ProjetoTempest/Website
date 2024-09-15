from decouple import config
from fastapi import status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt

from app.schemas.token import TokenData

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")


def generate_token(client):
    """
    Gera um token de acesso usando os dados de um cliente
    """
    return TokenData(
        # id=client.id,
        # name=client.name,
        # email=client.email,
        role_name=client.role_name,
    )


def encode_token(data_token: TokenData) -> str:
    """
    Codifica um dicionário em um token jwt

    Chaves do Token:
        - id:str
        - name: str
        - email: str
        - level: str
    """
    return jwt.encode(data_token.dict(), SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decodifica um token jwt em um dicionário com seu conteúdo

    Chaves do Token:
        - id: str
        - name: str
        - email: str
        - level: str
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

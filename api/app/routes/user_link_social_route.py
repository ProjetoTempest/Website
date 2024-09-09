from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.schemas.user_link_social import Request, Response, Update
from app.use_cases.user_link_social import UserLinkSocialCases as Case

router = APIRouter(prefix="/user_link_social")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_entity(
    entity: Request,
    db: Session = Depends(get_db)
):
    """
    Cria um novo produto na aplicação.

    Este endpoint recebe os dados do produto e cria um novo registro no banco de dados.
    Se o título já estiver registrado, retorna um erro 400.

    Args:
        entity (Request): Um objeto que contém os dados do produto a ser criado.
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        dict: Uma mensagem de sucesso.

    Raises:
        HTTPException: Se o título já estiver registrado, retorna uma exceção HTTP 400.
    """
    
    return Case(db_session=db).add(entity)

@router.get("/{entity_id}", response_model=Response)
def read_entity(entity_id: str, db: Session = Depends(get_db)):
    """
    Obtém um produto pelo ID.

    Este endpoint recebe um ID de produto e retorna os detalhes do produto correspondente.
    Se o produto não for encontrado, retorna um erro 404.

    Args:
        entity_id (str): O ID do produto a ser recuperado.
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        Re]
sResponse: Um objeto que representa os detalhes do produto.

    Raises:
        HTTPException: Se o produto não for encontrado, retorna uma exceção HTTP 404.
    """
    return Case(db_session=db).get(entity_id)


@router.get("/all/", status_code=status.HTTP_200_OK, response_model=list[Response])
def read_entitys(db: Session = Depends(get_db)):
    """
    Obtém todos os produtos.

    Este endpoint retorna uma lista com todos os produtos registrados no banco de dados.

    Args:
        db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        list[Re]
sResponse]: Uma lista de objetos que representam os produtos registrados.
    """

    return Case(db_session=db).get_all()


@router.put("/update/", status_code=status.HTTP_200_OK)
def update_entity(entity_update: Update, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um produto.

    Este endpoint atualiza os dados de um produto existente. Apenas os campos fornecidos (não `None`)
    serão atualizados. Se o produto não for encontrado, retorna um erro 404.

    Args:
        entity_update (Update): Os dados atualizados do produto.
        db (Session): A sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        dict: Uma mensagem de sucesso.
    """
    
    return Case(db_session=db).update(entity_update)


@router.delete("/delete/")
def delete_entity(id: str, db: Session = Depends(get_db)):
    """
    Deleta um produto com base no ID fornecido.

    Args:
        id (str): O ID do produto a ser deletado.
        db (Session): A sessão do banco de dados, fornecida automaticamente pelo FastAPI.

    Raises:
        HTTPException: Se o produto não for encontrado, retorna uma exceção HTTP 404.

    Returns:
        dict: Um dicionário com uma mensagem de sucesso e o status HTTP 200.
    """

    return Case(db_session=db).delete(entity_id=id)

from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, models
from ..controllers import social_network_controller  

routerSocialNetwork = APIRouter(prefix="/social_network")

@routerSocialNetwork.post("/")
async def create_social_network(
    social_network: schemas.SocialNetworkBase,    
    db: Session = Depends(get_db)
):
    """
    Rota para criar um nova rede social no banco de dados.

    Args:
    - social_network(schemas.SocialNetworkBase): Dados para criar a rede social.
    - db (Session): Sessão do banco de dados para executar a operação de criação.

    Returns:
    - models.SocialNetwork: Objeto do rede social criado no banco de dados.
    """
    
    flag_social = social_network_controller.get_social_network(db=db, social_id=social_network.id)
    print("Antes da flag")
    print(flag_social)
    
    if flag_social is not None:
        raise HTTPException(status_code=400, detail="Rede social já foi criada")
    
    return social_network_controller.create_social_network(db=db, social=social_network)

@routerSocialNetwork.get("/{social_id}")
def read_social(social_id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar uma rede social específica no banco de dados pelo seu ID.

    Args:
    - social_id (int): O ID da rede social que se deseja buscar.
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - models.SocialNetwork: Objeto da rede social encontrada no banco de dados.

    Raises:
    - HTTPException(404): Retorna um erro 404 se a rede social não for encontrada no banco de dados.
    """
    social = social_network_controller.get_social_network(db, social_id=social_id)
    if social is None:
        raise HTTPException(status_code=404, detail="Social not found")
    return social

@routerSocialNetwork.get("/")
def read_all_social(db: Session = Depends(get_db)):
    """
    Rota para buscar todas as redes sociais no banco de dados.

    Args:
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - List[models.SocialNetwork]: Lista de todas as redes sociais presentes no banco de dados.
    """
    return social_network_controller.get_all_social_network(db)

@routerSocialNetwork.put("/update/{social_id}", response_model=schemas.SocialNetworkBase)
def update_social(social_id: int, social: schemas.SocialNetworkUpdate, db: Session = Depends(get_db)):
    """
    Rota para atualizar uma rede social específico no banco de dados pelo seu ID.

    Args:
    - social_id (int): O ID da rede social que se deseja atualizar.
    - social (schemas.SocialNetworkUpdate): Dados atualizados da rede social a serem aplicados.
    - db (Session): Sessão do banco de dados para executar a operação de atualização.

    Returns:
    - schemas.SocialNetworkBase: Dados da rede social atualizado, conforme definido no esquema `schemas.SocialNetworkBase`.

    Raises:
    - HTTPException(404): Retorna um erro 404 se oa rede social não for encontrado no banco de dados.
    """
    db_social = social_network_controller.get_social_network(db=db, social_id=social_id)
    if db_social:
        return social_network_controller.update_social(db=db, db_social=db_social, social_update=social)    
    raise HTTPException(status_code=404, detail="Social not found")


@routerSocialNetwork.delete("/delete/{social_id}")
def delete_social(social_id: int, db: Session = Depends(get_db)):
    """
    Rota para excluir uma rede social específico do banco de dados pelo seu ID.

    Args:
    - social_id (int): O ID da rede social que se deseja excluir.
    - db (Session): Sessão do banco de dados para executar a operação de exclusão.

    Returns:
    - dict: Um dicionário com uma mensagem de sucesso e um status code 200 indicando que a rede social foi excluído com sucesso.

    Raises:
    - HTTPException(404): Retorna um erro 404 se a rede social não for encontrado no banco de dados.
    """
    flag = social_network_controller.delete_social(db=db, social_id=social_id)
    if flag == 0:
        raise HTTPException(status_code=404, detail="Social not found")
    return {"message": "Social deleted successfully", "status": 200}








from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, models
from ..controllers import user_link_social_network_controller, social_network_controller, user_controller

route_user_link_social = APIRouter(prefix="/user_link_social")

@route_user_link_social.post("/create_link_socil_user/{social_id}/{user_id}")
def create_link_social_user(social_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Cria um link entre uma rede social e um usuário.

    Args:
        social_id (int): ID da rede social.
        user_id (int): ID do usuário.
        db (Session): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        dict: Mensagem indicando que o link foi criado com sucesso.

    Raises:
        HTTPException: Se o usuário ou a rede rede social não forem encontrados, retorna status code 404.
        HTTPException: Se o link já tiver sido criado anteriormente, retorna status code 400.
    """
    social_db = social_network_controller.get_social_network(db=db, social_id=social_id)
    user = user_controller.get_user(db=db, user_id=user_id)

    if user is None or social_db is None:
        raise HTTPException(status_code=404, detail="Usuário ou rede social não encontrado")
    if user_link_social_network_controller.get_relacao_social_user_create(db=db, id_user=user_id, id_social=social_id) is not None:
        raise HTTPException(status_code=400, detail="Link já foi criado anteriormente")

    user_link_social_network_controller.create_link_social_user(db=db, social_id=social_id, user_id=user_id)
    return {"message": "Link criado com sucesso"}


@route_user_link_social.get("/get_relacao_social_user/")
def get_all_relacao_social_user(db: Session = Depends(get_db)):
    """
    Retorna todas as relações entre usuários e rede social no banco de dados.

    Args:
        db (Session): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        List[models.IntermediariaUsersocials]: Lista de objetos representando todas as relações entre usuários e rede social.
    """
    relacao = user_link_social_network_controller.get_all_relacao_social_user(db=db)
    return relacao

@route_user_link_social.get("/get_relacao_social_user/{id_relacao}")
def get_relacao_social_user_id(id_relacao: int, db: Session = Depends(get_db)):
    """
    Retorna a relação entre usuário e serviço com base no ID da relação.

    Args:
        id_relacao (int): ID da relação entre usuário e serviço.
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        schemas.IntermediariaUsersocials: Objeto representando a relação entre usuário e serviço com o ID especificado.

    Raises:
        HTTPException: Se a relação não for encontrada, retorna status code 404.
    """
    relacao = user_link_social_network_controller.get_relacao_social_user_id(db=db, id=id_relacao)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return relacao

@route_user_link_social.get("/get_socials_by_user/{user_id}")
def get_services_user(user_id: int, db: Session = Depends(get_db)):
    """
    Esta rota retorna todos as redes sociais associadas a um usuário específico.

    Args:
        user_id (int): ID do usuário para o qual deseja-se recuperar as redes sociais.
        db (Session, opcional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.SocialNetworkBase]: Uma lista de objetos `SocialNetworkBase` que representam as redes sociais associadas ao usuário.

    Raises:
        HTTPException: Se o usuário não for encontrado (status_code 404).
    """
    user = user_controller.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    services = user_link_social_network_controller.get_social_by_user(db=db, user_id=user.id)
    return services

@route_user_link_social.get("/get_user_by_social/{social_id}", response_model=list[schemas.UserBase])
def get_user_social(social_id: int, db: Session = Depends(get_db)):
    """
    Retorna todos os usuários associados a uma rede social específico.

    Args:
        social_id (int): ID da rede social para o qual deseja-se recuperar os usuários.
        db (Session, opcional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.UserBase]: Uma lista de objetos `UserBase` que representam os usuários associados a rede social.

    Raises:
        HTTPException: Se oa rede social não for encontrado (status_code 404).
    """
    social = social_network_controller.get_social_network(db=db, social_id=social_id)
    if social is None:
        raise HTTPException(status_code=404, detail="Rede social não encontrado")
    return user_link_social_network_controller.get_user_by_social(db=db, social_id=social.id)

@route_user_link_social.put("/update_link_user_social/{social_id}")
def update_link_user_social(social_id: int, user_link_social_update: schemas.UserSocialNetworkUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um da relação.

    Este endpoint atualiza os dados de um da relação existente. Apenas os campos fornecidos (não `None`)
    serão atualizados. Se a relação não for encontrado, retorna um erro 404.

    Args:
        social_id (int): O ID do da relação a ser atualizado.
        user_link_social_update (schemas.UserSocialNetworkUpdate): Os dados atualizados da relação.
        db (Session): A sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        schemas.SocialNetwork: Os dados da relação atualizado.
    """
    relacao = user_link_social_network_controller.get_relacao_social_user_id(db, id=social_id)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Link not found")
    
    print(relacao)
    update_rela = user_link_social_network_controller.update_social_fields(db=db, db_user_social=relacao, social_update=user_link_social_update)

    return update_rela

@route_user_link_social.delete("/delete_link_social_user/{id_relacao}")
def delete_link_social_user(id_relacao: int, db: Session = Depends(get_db)):
    """
    Endpoint para deletar uma relação entre usuário e rede social do banco de dados.

    Args:
        id_relacao (int): ID da relação entre usuário e rede social que deseja-se remover.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        dict: Um dicionário contendo uma mensagem de sucesso e o status HTTP 200 se a relação foi removida com sucesso.

    Raises:
        HTTPException: Retorna um erro 404 se a relação não for encontrada no banco de dados.
    """
    relacao = user_link_social_network_controller.delete_link_social_user(db=db, id=id_relacao)
    if relacao == 0:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return {"message": "Relação deletada com sucesso", "status": 200}
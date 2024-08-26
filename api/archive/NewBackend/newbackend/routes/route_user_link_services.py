from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List

from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, models
from ..controllers import user_link_services_controller, service_controller, user_controller

route_user_link_services = APIRouter(prefix="/user_link_services")

@route_user_link_services.post("/create_link_service_user/{service_id}/{user_id}")
def create_link_service_user(service_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Cria um link entre um serviço e um usuário.

    Args:
        service_id (int): ID do serviço.
        user_id (int): ID do usuário.
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        dict: Mensagem indicando que o link foi criado com sucesso.

    Raises:
        HTTPException: Se o usuário ou serviço não forem encontrados, retorna status code 404.
        HTTPException: Se o link já tiver sido criado anteriormente, retorna status code 400.
    """
    svc = service_controller.get_service(db=db, service_id=service_id)
    user = user_controller.get_user(db=db, user_id=user_id)

    if user is None or svc is None:
        raise HTTPException(status_code=404, detail="Usuário ou serviço não encontrado")
    if user_link_services_controller.get_relacao_service_user_create(db=db, id_user=user_id, id_service=service_id) is not None:
        raise HTTPException(status_code=400, detail="Link já foi criado anteriormente")

    user_link_services_controller.create_link_service_user(db=db, service_id=service_id, user_id=user_id)
    return {"message": "Link criado com sucesso"}

@route_user_link_services.get("/get_relacao_service_user/")
def get_all_relacao_service_user(db: Session = Depends(get_db)):
    """
    Retorna todas as relações entre usuários e serviços no banco de dados.

    Args:
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        List[models.IntermediariaUserServices]: Lista de objetos representando todas as relações entre usuários e serviços.
    """
    relacao = user_link_services_controller.get_all_relacao_service_user(db=db)
    return relacao

@route_user_link_services.get("/get_relacao_service_user/{id_relacao}", response_model=schemas.IntermediariaUserServices)
def get_relacao_service_user_id(id_relacao: int, db: Session = Depends(get_db)):
    """
    Retorna a relação entre usuário e serviço com base no ID da relação.

    Args:
        id_relacao (int): ID da relação entre usuário e serviço.
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        schemas.IntermediariaUserServices: Objeto representando a relação entre usuário e serviço com o ID especificado.

    Raises:
        HTTPException: Se a relação não for encontrada, retorna status code 404.
    """
    relacao = user_link_services_controller.get_relacao_service_user_id(db=db, id=id_relacao)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return relacao

@route_user_link_services.get("/get_services_by_user/{user_id}", response_model=list[schemas.ServiceBase])
def get_services_user(user_id: int, db: Session = Depends(get_db)):
    """
    Esta rota retorna todos os serviços associados a um usuário específico.

    Args:
        user_id (int): ID do usuário para o qual deseja-se recuperar os serviços.
        db (Session, opcional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.ServiceBase]: Uma lista de objetos `ServiceBase` que representam os serviços associados ao usuário.

    Raises:
        HTTPException: Se o usuário não for encontrado (status_code 404).
    """
    user = user_controller.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    services = user_link_services_controller.get_services_by_user(db=db, user_id=user.id)
    return services

@route_user_link_services.get("/get_user_by_service/{service_id}", response_model=list[schemas.UserBase])
def get_user_service(service_id: int, db: Session = Depends(get_db)):
    """
    Retorna todos os usuários associados a um serviço específico.

    Args:
        service_id (int): ID do serviço para o qual deseja-se recuperar os usuários.
        db (Session, opcional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.UserBase]: Uma lista de objetos `UserBase` que representam os usuários associados ao serviço.

    Raises:
        HTTPException: Se o serviço não for encontrado (status_code 404).
    """
    service = service_controller.get_service(db=db, service_id=service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return user_link_services_controller.get_user_by_service(db=db, service_id=service.id)

@route_user_link_services.put("/update_userid_link_service/{id_relacao}/{user_id}", response_model=schemas.IntermediariaUserServices)
def update_userid_link_service(id_relacao: int, user_id: int, db: Session = Depends(get_db)):
    """
    Atualiza o ID do usuário em uma relação específica entre usuário e serviço.

    Args:
        id_relacao (int): ID da relação entre usuário e serviço que deseja-se atualizar.
        user_id (int): Novo ID do usuário para atualização na relação.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        schemas.IntermediariaUserServices: Objeto que representa a relação usuário-serviço atualizada.

    Raises:
        HTTPException: Se o usuário não for encontrado com o ID especificado.
        HTTPException: Se a relação entre usuário e serviço não for encontrada com o ID especificado.
    """
    user = user_controller.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    relacao = user_link_services_controller.update_userid_link_service(db=db, id_relacao=id_relacao, id_user=user_id)

    if relacao is None:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return relacao

@route_user_link_services.put("/update_serviceid_link_user/{id_relacao}/{service_id}", response_model=schemas.IntermediariaUserServices)
def update_serviceid_link_user(id_relacao: int, service_id: int, db: Session = Depends(get_db)):
    """
    Atualiza o ID do serviço em uma relação específica entre usuário e serviço.

    Args:
        id_relacao (int): ID da relação entre usuário e serviço que deseja-se atualizar.
        service_id (int): Novo ID do serviço para atualização na relação.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        schemas.IntermediariaUserServices: Objeto que representa a relação usuário-serviço atualizada.

    Raises:
        HTTPException: Se o serviço não for encontrado com o ID especificado.
        HTTPException: Se a relação entre usuário e serviço não for encontrada com o ID especificado.
    """
    service = service_controller.get_service(db=db, service_id=service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    relacao = user_link_services_controller.update_serviceid_link_user(db=db, id_relacao=id_relacao, id_service=service_id)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return relacao

@route_user_link_services.delete("/delete_link_service_user/{id_relacao}")
def delete_link_service_user(id_relacao: int, db: Session = Depends(get_db)):
    """
    Endpoint para deletar uma relação entre usuário e serviço do banco de dados.

    Args:
        id_relacao (int): ID da relação entre usuário e serviço que deseja-se remover.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        dict: Um dicionário contendo uma mensagem de sucesso e o status HTTP 200 se a relação foi removida com sucesso.

    Raises:
        HTTPException: Retorna um erro 404 se a relação não for encontrada no banco de dados.
    """
    relacao = user_link_services_controller.delete_link_service_user(db=db, id=id_relacao)
    if relacao == 0:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return {"message": "Relação deletada com sucesso", "status": 200}

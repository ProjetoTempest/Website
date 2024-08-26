from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas
from ..controllers import user_link_tecnologia_controller, tecnologia_controller, user_controller

route_user_link_tec = APIRouter(prefix="/user_link_tec")

@route_user_link_tec.post("/create_link_tec_user/{tec_id}/{user_id}")
def create_link_tec_user(tec_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Cria um link entre uma tecnologia e um usuário.

    Args:
        tec_id (int): ID da tecnologia.
        user_id (int): ID do usuário.
        db (Session): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        dict: Mensagem indicando que o link foi criado com sucesso.

    Raises:
        HTTPException: Se o usuário ou a tecnologia não forem encontrados, retorna status code 404.
        HTTPException: Se o link já tiver sido criado anteriormente, retorna status code 400.
    """
    tec_db = tecnologia_controller.get_tecno(db=db, tec_id=tec_id)
    user = user_controller.get_user(db=db, user_id=user_id)

    if user is None or tec_db is None:
        raise HTTPException(status_code=404, detail="Usuário ou tecnologia não encontrado")
    if user_link_tecnologia_controller.get_relacao_tec_user_create(db=db, id_user=user_id, id_tec=tec_id) is not None:
        raise HTTPException(status_code=400, detail="Link já foi criado anteriormente")

    user_link_tecnologia_controller.create_link_tec_user(db=db, tec_id=tec_id, user_id=user_id)
    return {"message": "Link criado com sucesso"}


@route_user_link_tec.get("/get_relacao_tec_user/")
def get_all_relacao_tec_user(db: Session = Depends(get_db)):
    """
    Retorna todas as relações entre usuários e tecnologia no banco de dados.

    Args:
        db (Session): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        List[models.IntermediariaUserTecs]: Lista de objetos representando todas as relações entre usuários e tecnologia.
    """
    relacao = user_link_tecnologia_controller.get_all_relacao_tec_user(db=db)
    return relacao

@route_user_link_tec.get("/get_relacao_tec_user/{id_relacao}")
def get_relacao_tec_user_id(id_relacao: int, db: Session = Depends(get_db)):
    """
    Retorna a relação entre usuário e tecnologia com base no ID da relação.

    Args:
        id_relacao (int): ID da relação entre usuário e tecnologia.
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        schemas.IntermediariaUserTecs: Objeto representando a relação entre usuário e tecnologia com o ID especificado.

    Raises:
        HTTPException: Se a relação não for encontrada, retorna status code 404.
    """
    relacao = user_link_tecnologia_controller.get_relacao_tec_user_id(db=db, id=id_relacao)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return relacao

@route_user_link_tec.get("/get_tecs_by_user/{user_id}")
def get_tecs_user(user_id: int, db: Session = Depends(get_db)):
    """
    Esta rota retorna todas as tecnologias associadas a um usuário específico.

    Args:
        user_id (int): ID do usuário para o qual deseja-se recuperar as tecnologias.
        db (Session, opcional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.TecBase]: Uma lista de objetos `TecBase` que representam as tecnologias associadas ao usuário.

    Raises:
        HTTPException: Se o usuário não for encontrado (status_code 404).
    """
    user = user_controller.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    tecs = user_link_tecnologia_controller.get_tec_by_user(db=db, user_id=user.id)
    return tecs

@route_user_link_tec.get("/get_user_by_tec/{tec_id}", response_model=list[schemas.UserBase])
def get_user_tec(tec_id: int, db: Session = Depends(get_db)):
    """
    Retorna todos os usuários associados a uma tecnologia específica.

    Args:
        tec_id (int): ID da tecnologia para o qual deseja-se recuperar os usuários.
        db (Session, opcional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.UserBase]: Uma lista de objetos `UserBase` que representam os usuários associados à tecnologia.

    Raises:
        HTTPException: Se a tecnologia não for encontrada (status_code 404).
    """
    tec = tecnologia_controller.get_tecno(db=db, tec_id=tec_id)
    if tec is None:
        raise HTTPException(status_code=404, detail="Tecnologia não encontrada")
    return user_link_tecnologia_controller.get_user_by_tec(db=db, tec_id=tec.id)

@route_user_link_tec.put("/update_link_user_tec/{tec_id}")
def update_link_user_tec(tec_id: int, user_link_tec_update: schemas.UserTecnologiaUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de uma relação.

    Este endpoint atualiza os dados de uma relação existente. Apenas os campos fornecidos (não `None`)
    serão atualizados. Se a relação não for encontrada, retorna um erro 404.

    Args:
        tec_id (int): O ID da relação a ser atualizada.
        user_link_tec_update (schemas.UserTecnologiaUpdate): Os dados atualizados da relação.
        db (Session): A sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        schemas.Tec: Os dados da relação atualizada.
    """
    relacao = user_link_tecnologia_controller.get_relacao_tec_user_id(db, id=tec_id)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    
    print(relacao)
    update_rela = user_link_tecnologia_controller.update_tec_fields(db=db, db_user_tec=relacao, tec_update=user_link_tec_update)

    return update_rela

@route_user_link_tec.delete("/delete_link_tec_user/{id_relacao}")
def delete_link_tec_user(id_relacao: int, db: Session = Depends(get_db)):
    """
    Endpoint para deletar uma relação entre usuário e tecnologia do banco de dados.

    Args:
        id_relacao (int): ID da relação entre usuário e tecnologia que deseja-se remover.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        dict: Um dicionário contendo uma mensagem de sucesso e o status HTTP 200 se a relação foi removida com sucesso.

    Raises:
        HTTPException: Retorna um erro 404 se a relação não for encontrada no banco de dados.
    """
    relacao = user_link_tecnologia_controller.delete_link_tec_user(db=db, id=id_relacao)
    if relacao == 0:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return {"message": "Relação deletada com sucesso", "status": 200}

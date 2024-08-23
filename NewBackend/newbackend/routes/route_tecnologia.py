from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, models
from ..controllers import tecnologia_controller

routerTecnologia = APIRouter(prefix="/tecnologia")

@routerTecnologia.post("/")
async def create_tecno(
    tec: schemas.TecnologiaBase,    
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
    
    # flag_tec = tecnologia_controller.get_tecno(db=db, tec_id=tec.id)
    # print("Antes da flag")
    # print(flag_tec)
    
    # if flag_tec is not None:
    #     raise HTTPException(status_code=400, detail="Rede social já foi criada")
    
    return tecnologia_controller.create_tecno(db=db, tec=tec)

@routerTecnologia.get("/{tec_id}")
def read_tecno(tec_id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar uma rede tec específica no banco de dados pelo seu ID.

    Args:
    - tec_id (int): O ID da rede tec que se deseja buscar.
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - models.tecNetwork: Objeto da rede tec encontrada no banco de dados.

    Raises:
    - HTTPException(404): Retorna um erro 404 se a rede tec não for encontrada no banco de dados.
    """
    tec = tecnologia_controller.get_tecno(db, tec_id=tec_id)
    if tec is None:
        raise HTTPException(status_code=404, detail="tec not found")
    return tec

@routerTecnologia.get("/")
def read_all_tec(db: Session = Depends(get_db)):
    """
    Rota para buscar todas as redes sociais no banco de dados.

    Args:
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - List[models.SocialNetwork]: Lista de todas as redes sociais presentes no banco de dados.
    """
    return tecnologia_controller.get_all_tecno(db)

@routerTecnologia.put("/update/{tec_id}", response_model=schemas.TecnologiaBase)
def update_tec(tec_id: int, tec: schemas.TecnologiaUpdate, db: Session = Depends(get_db)):
    """
    Rota para atualizar uma rede tec específico no banco de dados pelo seu ID.

    Args:
    - tec_id (int): O ID da rede tec que se deseja atualizar.
    - tec (schemas.tecNetworkUpdate): Dados atualizados da rede tec a serem aplicados.
    - db (Session): Sessão do banco de dados para executar a operação de atualização.

    Returns:
    - schemas.tecNetworkBase: Dados da rede tec atualizado, conforme definido no esquema `schemas.tecNetworkBase`.

    Raises:
    - HTTPException(404): Retorna um erro 404 se oa rede tec não for encontrado no banco de dados.
    """
    db_tec = tecnologia_controller.get_tecno(db=db, tec_id=tec_id)
    if db_tec:
        return tecnologia_controller.update_tecno(db=db, db_tec=db_tec, tec_update=tec)    
    raise HTTPException(status_code=404, detail="Tec not found")


@routerTecnologia.delete("/delete/{tec_id}")
def delete_tec(tec_id: int, db: Session = Depends(get_db)):
    """
    Rota para excluir uma rede tec específico do banco de dados pelo seu ID.

    Args:
    - tec_id (int): O ID da rede tec que se deseja excluir.
    - db (Session): Sessão do banco de dados para executar a operação de exclusão.

    Returns:
    - dict: Um dicionário com uma mensagem de sucesso e um status code 200 indicando que a rede tec foi excluído com sucesso.

    Raises:
    - HTTPException(404): Retorna um erro 404 se a rede tec não for encontrado no banco de dados.
    """
    flag = tecnologia_controller.delete_tecno(db=db, tec_id=tec_id)
    if flag == 0:
        raise HTTPException(status_code=404, detail="tec not found")
    return {"message": "tec deleted successfully", "status": 200}








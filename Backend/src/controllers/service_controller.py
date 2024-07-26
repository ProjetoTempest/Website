from sqlalchemy.orm import Session, joinedload
from .. import schemas, models

def create_service(db: Session, service: dict):
    """
    Cria um novo serviço no banco de dados com base nos dados fornecidos.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - service (dict): Um dicionário contendo os dados do serviço a ser criado.
      Deve conter as chaves "title", "description", "value" e "images".

    Returns:
    - models.Service: O objeto do serviço criado no banco de dados, incluindo as imagens associadas.
    """

    db_service = models.Service(title=service.title, description= service.description, value=service.value)

    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    lista_imgs = [models.ImagesService(url=url_img.url, item_id=db_service.id) for url_img in service.images]

    db.add_all(lista_imgs)
    db_service.images = lista_imgs

    db.commit()
    db.refresh(db_service)

    return db_service

    # service_data = {
    #     "title": service["title"],
    #     "description": service["description"],
    #     "value": service["value"]
    # }

    # # Crie a instância do serviço
    # db_service = models.Service(**service_data)
    # db.add(db_service)
    # db.commit()
    # db.refresh(db_service)

    # id_service = db_service.id

    # # Crie e adicione as instâncias de imagens associadas ao serviço
    # if service["images"]:
    #     list_imgs = []
    #     for img in service["images"]:
    #         img_schema = models.ImagesService(
    #             title=img,
    #             path=img,
    #             service_id=id_service
    #         )
    #         db.add(img_schema)
    #         list_imgs.append(img_schema)

    #     db.commit()

    # # Atualize o serviço com as imagens associadas
    # # db_service.images = list_imgs
    # db.commit()
    # db.refresh(db_service)

    return db_service


def get_services(db: Session):
    """
    Retorna todos os serviços do banco de dados.

    Args:
    - db (Session): A sessão do banco de dados para executar a consulta.

    Returns:
    - List[Service]: Uma lista de todos os serviços no banco de dados, cada serviço
      opcionalmente carregado com suas imagens associadas.
    """
    return db.query(models.Service).options(joinedload(models.Service.images)).all()


def get_service(db: Session, service_id: int):
    """
    Retorna um serviço com base no ID fornecido.

    Args:
        db (Session): A sessão do banco de dados.
        service_id (int): O ID do serviço.

    Returns:
        models.Service | None: O serviço encontrado ou None se nenhum serviço corresponder ao ID fornecido.
    """
    return db.query(models.Service).filter(models.Service.id == service_id).options(joinedload(models.Service.images)).first()


def update_service(db: Session, db_service: models.Service, service_update: schemas.ServiceUpdate):
    """
    Atualiza um serviço existente no banco de dados com base nos dados fornecidos.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - db_service (models.Service): O serviço no banco de dados que será atualizado.
    - service_update (schemas.ProductUpdate): Os dados atualizados do serviço.

    Returns:
    - models.Service: O objeto do serviço atualizado no banco de dados.
    """
    update_data = service_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        match key:
            case "title":
                db_service.title = value
            case "description":
                db_service.description = value
            case "value":
                db_service.value = value

    db.commit()
    db.refresh(db_service)
    return db_service


def delete_service(db: Session, service_id: int):
    """
    Remove um serviço do banco de dados com base no ID fornecido.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - service_id (int): O ID do serviço que deve ser removido.

    Returns:
    - int: O número de registros afetados pela operação de exclusão.
      Retorna 1 se o serviço foi encontrado e removido com sucesso,
      ou 0 se nenhum serviço correspondente ao ID foi encontrado.
    """
    flag = db.query(models.Service).filter(models.Service.id == service_id).delete()
    db.commit()

    return flag

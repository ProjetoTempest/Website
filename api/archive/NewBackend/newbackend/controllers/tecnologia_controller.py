from sqlalchemy.orm import Session, joinedload
from .. import schemas, models


def create_tecno(db: Session, tec: schemas.TecnologiaBase):
    tec = tec.model_dump()
    tec = models.Tecnologia(**tec)
    db.add(tec)
    db.commit()
    db.refresh(tec)

    return tec

def get_tecno(db: Session, tec_id: int):
    """
    Retorna um a rede tec com base no ID fornecido.

    Args:
        db (Session): A sessão do banco de dados.
        tec_id (int): O ID do a rede tec.

    Returns:
        models.Tecnologia | None: A rede tec encontrada ou None se nenhum a rede tec corresponder ao ID fornecido.
    """
    return db.query(models.Tecnologia).filter(models.Tecnologia.id == tec_id).first()

def get_all_tecno(db: Session):
    """
    Retorna todas as redes sociais do banco de dados.

    Args:
        db (Session): A sessão do banco de dados.

    Returns:
        List[models.Tecnologia] | None: Uma lista de todas as redes sociais no banco de dados ou None se nenhuma rede tec.
    """
    return db.query(models.Tecnologia).all()

def update_tecno(db: Session, db_tec: models.Tecnologia, tec_update: schemas.TecnologiaUpdate):
    """
    Atualiza uma rede tec existente no banco de dados com base nos dados fornecidos.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - db_tec (models.Tecnologia): A rede tec no banco de dados que será atualizado.
    - tec_update (schemas.TecnologiaUpdate): Os dados atualizados da rede tec.

    Returns:
    - models.Tecnologia: O objeto da rede tec atualizado no banco de dados.
    """
    update_data = tec_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        match key:
            case "title":
                db_tec.title = value
            case "description":
                db_tec.description = value
            case "link":
                db_tec.link = value
            case "icon":
                db_tec.icon = value

    db.commit()
    db.refresh(db_tec)
    return db_tec

def delete_tecno(db: Session, tec_id: int):
    flag = db.query(models.Tecnologia).filter(models.Tecnologia.id == tec_id).delete()
    db.commit()
    return flag
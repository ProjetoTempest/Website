from sqlalchemy.orm import Session
from .. import schemas, models


def create_social_network(db: Session, social: schemas.SocialNetworkBase):
    social = social.model_dump()
    social = models.SocialNetwork(**social)
    db.add(social)
    db.commit()
    db.refresh(social)

    return social

def get_social_network(db: Session, social_id: int):
    """
    Retorna um a rede social com base no ID fornecido.

    Args:
        db (Session): A sessão do banco de dados.
        social_id (int): O ID do a rede social.

    Returns:
        models.SocialNetwork | None: A rede social encontrada ou None se nenhum a rede social corresponder ao ID fornecido.
    """
    return db.query(models.SocialNetwork).filter(models.SocialNetwork.id == social_id).first()

def get_all_social_network(db: Session):
    """
    Retorna todas as redes sociais do banco de dados.

    Args:
        db (Session): A sessão do banco de dados.

    Returns:
        List[models.SocialNetwork] | None: Uma lista de todas as redes sociais no banco de dados ou None se nenhuma rede social.
    """
    return db.query(models.SocialNetwork).all()

def update_social(db: Session, db_social: models.SocialNetwork, social_update: schemas.SocialNetworkUpdate):
    """
    Atualiza uma rede social existente no banco de dados com base nos dados fornecidos.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - db_social (models.SocialNetwork): A rede social no banco de dados que será atualizado.
    - social_update (schemas.SocialNetworkUpdate): Os dados atualizados da rede social.

    Returns:
    - models.SocialNetwork: O objeto da rede social atualizado no banco de dados.
    """
    update_data = social_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        match key:
            case "title":
                db_social.title = value
            case "description":
                db_social.description = value
            case "link":
                db_social.link = value
            case "icon":
                db_social.icon = value

    db.commit()
    db.refresh(db_social)
    return db_social

def delete_social(db: Session, social_id: int):
    flag = db.query(models.SocialNetwork).filter(models.SocialNetwork.id == social_id).delete()
    db.commit()
    return flag
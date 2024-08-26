from sqlalchemy.orm import Session
from .. import models, schemas

def create_link_tec_user(db: Session, tec_id: int, user_id: int):
    """
    Cria um link entre um usuário e um serviço no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        tec_id (int): ID do serviço.
        user_id (int): ID do usuário.

    Returns:
        models.IntermediariaUserServices: Objeto representando a nova relação criada entre usuário e serviço.
    """
    db_tec_user = models.UserTecnologia(user_id=user_id, tecnologia_id=tec_id)
    db.add(db_tec_user)
    db.commit()
    db.refresh(db_tec_user)

    return db_tec_user

def get_relacao_tec_user_create(db: Session, id_user: int, id_tec: int):
    """
    Obtém a relação entre um usuário e uma tecnologia específica.

    Args:
        db (Session): Sessão do banco de dados.
        id_user (int): ID do usuário.
        id_tec (int): ID da tecnologia.

    Returns:
        Optional[models.UserTecnologia]: Objeto representando a relação entre usuário e tecnologia,
        ou None se não existir.

    """

    return db.query(models.UserTecnologia).\
            filter(models.UserTecnologia.user_id == id_user,
            models.UserTecnologia.tecnologia_id == id_tec).\
            first()

def get_all_relacao_tec_user(db: Session):
    """
    Obtém todas as relações entre usuários e tecnologias armazenadas no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.

    Returns:
        List[models.UserTecnologia]: Lista contendo todos os objetos representando as relações
        entre usuários e tecnologias.
    """
    return db.query(models.UserTecnologia).all()

def get_relacao_tec_user_id(db: Session, id: int):
    """
    Obtém a relação entre um usuário e uma tecnologia com base no ID da relação.

    Args:
        db (Session): Sessão do banco de dados.
        id (int): ID da relação entre usuário e tecnologia.

    Returns:
        Optional[models.UserTecnologia]: Objeto representando a relação entre usuário e tecnologia com o ID especificado, ou None se não existir.
    """
    return db.query(models.UserTecnologia).filter(models.UserTecnologia.id == id).first()

def get_tec_by_user(db: Session, user_id: int):
    """
    Retorna todas as tecnologias associadas a um usuário específico.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy.
        user_id (int): ID do usuário para o qual deseja-se recuperar as tecnologias.

    Returns:
        List[models.Tec]: Uma lista de objetos do tipo `Tec` associados ao usuário.
    """
    return db.query(models.Tecnologia).join(models.UserTecnologia).filter(models.UserTecnologia.user_id == user_id).all()

def get_user_by_tec(db: Session, tec_id: int):
    """
    Retorna todos os usuários associados a uma tecnologia específica.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy.
        tec_id (int): ID da tecnologia para o qual deseja-se recuperar os usuários.

    Returns:
        List[models.User]: Uma lista de objetos do tipo `User` que representam os usuários associados a tecnologia.
    """
    return db.query(models.User).join(models.UserTecnologia).filter(models.UserTecnologia.tecnologia_id == tec_id).all()

def update_tec_fields(db: Session, db_user_tec: models.UserTecnologia, tec_update: schemas.UserTecnologiaUpdate):
    """
    Atualiza os dados da relação de usuário a tecnologia.

    Args:
        db (Session): A sessão do banco de dados.
        db_user_tec (models.UserTecnologia): O objeto da relação existente.
        tec_update (schemas.UserTecnologiaUpdate): Os dados atualizados da relação.

    Returns:
        models.UserTecnologia: A relação atualizada.
    """

    update_data = tec_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        match key:
            case "user_id":
                db_user_tec.user_id = value
            case "tecnologia_id":
                db_user_tec.tecnologia_id = value

    db.commit()
    db.refresh(db_user_tec)
    return db_user_tec

def delete_link_tec_user(db: Session, id: int):
    """
    Deleta uma relação entre usuário e serviço do banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id (int): ID da relação entre usuário e serviço que deseja-se remover.

    Returns:
        int: Retorna o número de linhas afetadas pela operação de deleção. Deve ser 1 se a deleção for bem-sucedida.
    """
    flag = db.query(models.UserTecnologia).filter(models.UserTecnologia.id == id).delete()
    db.commit()
    return flag

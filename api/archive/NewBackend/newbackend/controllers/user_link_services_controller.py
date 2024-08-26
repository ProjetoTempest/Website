from sqlalchemy.orm import Session
from .. import models

def create_link_service_user(db: Session, service_id: int, user_id: int):
    """
    Cria um link entre um usuário e um serviço no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        service_id (int): ID do serviço.
        user_id (int): ID do usuário.

    Returns:
        models.IntermediariaUserServices: Objeto representando a nova relação criada entre usuário e serviço.
    """
    db_service_user = models.IntermediariaUserServices(user_id=user_id, service_id=service_id)
    db.add(db_service_user)
    db.commit()
    db.refresh(db_service_user)

    return db_service_user


def get_relacao_service_user_create(db: Session, id_user: int, id_service: int):
    """
    Obtém a relação entre um usuário e um serviço específico.

    Args:
        db (Session): Sessão do banco de dados.
        id_user (int): ID do usuário.
        id_service (int): ID do serviço.

    Returns:
        Optional[models.IntermediariaUserServices]: Objeto representando a relação entre usuário e serviço,
        ou None se não existir.

    """
    return db.query(models.IntermediariaUserServices).filter(models.IntermediariaUserServices.user_id == id_user, models.IntermediariaUserServices.service_id == id_service).first()

def get_all_relacao_service_user(db: Session):
    """
    Obtém todas as relações entre usuários e serviços armazenadas no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.

    Returns:
        List[models.IntermediariaUserServices]: Lista contendo todos os objetos representando as relações
        entre usuários e serviços.
    """
    return db.query(models.IntermediariaUserServices).all()

def get_relacao_service_user_id(db: Session, id: int):
    """
    Obtém a relação entre um usuário e um serviço com base no ID da relação.

    Args:
        db (Session): Sessão do banco de dados.
        id (int): ID da relação entre usuário e serviço.

    Returns:
        Optional[models.IntermediariaUserServices]: Objeto representando a relação entre usuário e serviço com o ID especificado,
        ou None se não existir.
    """
    return db.query(models.IntermediariaUserServices).filter(models.IntermediariaUserServices.id == id).first()


def get_user_by_service(db: Session, service_id: int):
    """
    Retorna todos os usuários associados a um serviço específico.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy.
        service_id (int): ID do serviço para o qual deseja-se recuperar os usuários.

    Returns:
        List[models.User]: Uma lista de objetos do tipo `User` que representam os usuários associados ao serviço.
    """
    return db.query(models.User).join(models.IntermediariaUserServices).filter(models.IntermediariaUserServices.service_id == service_id).all()

def update_userid_link_service(db: Session, id_relacao: int, id_user: int):
    """
    Atualiza o ID do usuário em uma relação entre usuário e serviço específica no banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id_relacao (int): ID da relação entre usuário e serviço que deseja-se atualizar.
        id_user (int): Novo ID do usuário para atualização na relação.

    Returns:
        Optional[models.IntermediariaUserServices]: Objeto que representa a relação usuário-serviço atualizada, ou None se a relação não for encontrada.
    """
    relacao = get_relacao_service_user_id(db=db, id=id_relacao)
    if relacao is not None:
        relacao.user_id = id_user
        db.commit()
        db.refresh(relacao)
        return relacao
    return None

def update_serviceid_link_user(db: Session, id_relacao: int, id_service: int):
    """
    Atualiza o ID do serviço em uma relação entre usuário e serviço específica no banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id_relacao (int): ID da relação entre usuário e serviço que deseja-se atualizar.
        id_service (int): Novo ID do serviço para atualização na relação.

    Returns:
        Optional[models.IntermediariaUserServices]: Objeto que representa a relação usuário-serviço atualizada, ou None se a relação não for encontrada.
    """
  
    relacao = get_relacao_service_user_id(db=db, id=id_relacao)
    if relacao is not None:
        relacao.service_id = id_service
        db.commit()
        db.refresh(relacao)
        return relacao
    return None

def delete_link_service_user(db: Session, id: int):
    """
    Deleta uma relação entre usuário e serviço do banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id (int): ID da relação entre usuário e serviço que deseja-se remover.

    Returns:
        int: Retorna o número de linhas afetadas pela operação de deleção. Deve ser 1 se a deleção for bem-sucedida.
    """
    flag = db.query(models.IntermediariaUserServices).filter(models.IntermediariaUserServices.id == id).delete()
    db.commit()
    return flag

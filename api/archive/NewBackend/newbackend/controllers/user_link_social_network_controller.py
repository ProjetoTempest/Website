from sqlalchemy.orm import Session
from .. import models, schemas

def create_link_social_user(db: Session, social_id: int, user_id: int):
    """
    Cria um link entre um usuário e um serviço no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        service_id (int): ID do serviço.
        user_id (int): ID do usuário.

    Returns:
        models.IntermediariaUserServices: Objeto representando a nova relação criada entre usuário e serviço.
    """
    db_social_user = models.UserSocialNetwork(user_id=user_id, social_network_id=social_id)
    db.add(db_social_user)
    db.commit()
    db.refresh(db_social_user)

    return db_social_user

def get_relacao_social_user_create(db:Session, id_user:int, id_social:int):
    """
    Obtém a relação entre um usuário e uma rede social específica.

    Args:
        db (Session): Sessão do banco de dados.
        id_user (int): ID do usuário.
        id_service (int): ID da rede social.

    Returns:
        Optional[models.UserSocialNetwork]: Objeto representando a relação entre usuário e rede social,
        ou None se não existir.

    """

    return db.query(models.UserSocialNetwork).\
            filter(models.UserSocialNetwork.user_id == id_user,
            models.UserSocialNetwork.social_network_id == id_social).\
            first()

def get_all_relacao_social_user(db: Session):
    """
    Obtém todas as relações entre usuários e redes social armazenadas no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.

    Returns:
        List[models.UserSocialNetwork]: Lista contendo todos os objetos representando as relações
        entre usuários e redes social.
    """
    return db.query(models.UserSocialNetwork).all()

def get_relacao_social_user_id(db:Session, id:int):
    """
    Obtém a relação entre um usuário e uma rede social com base no ID da relação.

    Args:
        db (Session): Sessão do banco de dados.
        id (int): ID da relação entre usuário e rede social.

    Returns:
        Optional[models.UserSocialNetwork]: Objeto representando a relação entre usuário e rede social com o ID especificado, ou None se não existir.
    """
    return db.query(models.UserSocialNetwork).filter(models.UserSocialNetwork.id == id).first()

def get_social_by_user(db: Session, user_id: int):
    """
    Retorna todos as redes sociais associados a um usuário específico.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy.
        user_id (int): ID do usuário para o qual deseja-se recuperar as redes sociais.

    Returns:
        List[models.SocialNetwork]: Uma lista de objetos do tipo `SocialNetwork` associados ao usuário.
    """
    return db.query(models.SocialNetwork).join(models.UserSocialNetwork).filter(models.UserSocialNetwork.user_id == user_id).all()

def get_user_by_social(db: Session, social_id: int):
    """
    Retorna todos os usuários associados a uma rede social específico.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy.
        social_id (int): ID da rede social para o qual deseja-se recuperar os usuários.

    Returns:
        List[models.User]: Uma lista de objetos do tipo `User` que representam os usuários associados a rede social.
    """
    return db.query(models.User).join(models.UserSocialNetwork).filter(models.UserSocialNetwork.social_network_id == social_id).all()

def update_social_fields(db: Session, db_user_social: models.UserSocialNetwork, social_update: schemas.UserSocialNetworkUpdate):
    """
    Atualiza os dados da relação de usuário a rede social.

    Args:
        db (Session): A sessão do banco de dados.
        db_user_social (models.UserSocialNetwork): O objeto da relação existente.
        social_update (schemas.UserSocialNetworkUpdate): Os dados atualizados da relação.

    Returns:
        models.UserSocialNetwork: A relação atualizada.
    """

    update_data = social_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        match key:
            case "user_id":
                db_user_social.user_id = value
            case "social_network_id":
                db_user_social.social_network_id = value

    db.commit()
    db.refresh(db_user_social)
    return db_user_social

def delete_link_social_user(db: Session, id: int):
    """
    Deleta uma relação entre usuário e serviço do banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id (int): ID da relação entre usuário e serviço que deseja-se remover.

    Returns:
        int: Retorna o número de linhas afetadas pela operação de deleção. Deve ser 1 se a deleção for bem-sucedida.
    """
    flag = db.query(models.UserSocialNetwork).filter(models.UserSocialNetwork.id == id).delete()
    db.commit()
    return flag

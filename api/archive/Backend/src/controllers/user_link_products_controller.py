from sqlalchemy.orm import Session
from .. import models

def create_link_product_user(db: Session, product_id: int, user_id: int):
    """
    Cria um link entre um usuário e um produto no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        product_id (int): ID do produto.
        user_id (int): ID do usuário.

    Returns:
        models.IntermediariaUserProducts: Objeto representando a nova relação criada entre usuário e produto.
    """
    db_product_user = models.IntermediariaUserProducts(user_id=user_id, products_id=product_id)
    db.add(db_product_user)
    db.commit()
    db.refresh(db_product_user)

    return db_product_user


def get_relacao_product_user_create(db: Session, id_user: int, id_product: int):
    """
    Obtém a relação entre um usuário e um produto específico.

    Args:
        db (Session): Sessão do banco de dados.
        id_user (int): ID do usuário.
        id_product (int): ID do produto.

    Returns:
        Optional[models.IntermediariaUserProducts]: Objeto representando a relação entre usuário e produto,
        ou None se não existir.

    """
    return db.query(models.IntermediariaUserProducts).filter(models.IntermediariaUserProducts.user_id == id_user, models.IntermediariaUserProducts.products_id == id_product).first()

def get_all_relacao_product_user(db: Session):
    """
    Obtém todas as relações entre usuários e produtos armazenadas no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.

    Returns:
        List[models.IntermediariaUserProducts]: Lista contendo todos os objetos representando as relações
        entre usuários e produtos.
    """
    return db.query(models.IntermediariaUserProducts).all()

def get_relacao_product_user_id(db: Session, id: int):
    """
    Obtém a relação entre um usuário e um produto com base no ID da relação.

    Args:
        db (Session): Sessão do banco de dados.
        id (int): ID da relação entre usuário e produto.

    Returns:
        Optional[models.IntermediariaUserProducts]: Objeto representando a relação entre usuário e produto com o ID especificado,
        ou None se não existir.
    """
    return db.query(models.IntermediariaUserProducts).filter(models.IntermediariaUserProducts.id == id).first()

def get_products_by_user(db: Session, user_id: int):
    """
    Retorna todos os produtos associados a um usuário específico.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy.
        user_id (int): ID do usuário para o qual deseja-se recuperar os produtos.

    Returns:
        List[models.Products]: Uma lista de objetos do tipo `Products` associados ao usuário.
    """
    return db.query(models.Products).join(models.IntermediariaUserProducts).filter(models.IntermediariaUserProducts.user_id == user_id).all()
    

def get_user_by_product(db: Session, product_id: int):
    """
    Retorna todos os usuários associados a um produto específico.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        product_id (int): ID do produto para o qual deseja-se recuperar os usuários.

    Returns:
        List[models.User]: Uma lista de objetos do tipo `User` que representam os usuários associados ao produto.
    """
    return db.query(models.User).join(models.IntermediariaUserProducts).filter(models.IntermediariaUserProducts.products_id == product_id).all()

def update_userid_link_product(db: Session, id_relacao: int, id_user: int):
    """
    Atualiza o ID do usuário em uma relação entre usuário e produto específica no banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id_relacao (int): ID da relação entre usuário e produto que deseja-se atualizar.
        id_user (int): Novo ID do usuário para atualização na relação.

    Returns:
        Optional[models.IntermediariaUserProducts]: Objeto que representa a relação usuário-produto atualizada, ou None se a relação não for encontrada.
    """
    relacao = get_relacao_product_user_id(db=db, id=id_relacao)
    if relacao is not None:
        relacao.user_id = id_user
        db.commit()
        db.refresh(relacao)
        return relacao
    return None
        

def update_produtid_link_user(db: Session, id_relacao: int, id_produt: int):
    """
    Atualiza o ID do produto em uma relação entre usuário e produto específica no banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id_relacao (int): ID da relação entre usuário e produto que deseja-se atualizar.
        id_product (int): Novo ID do produto para atualização na relação.

    Returns:
        Optional[models.IntermediariaUserProducts]: Objeto que representa a relação usuário-produto atualizada, ou None se a relação não for encontrada.
    """
  
    relacao = get_relacao_product_user_id(db=db, id=id_relacao)
    if relacao is not None:
        relacao.products_id = id_produt
        db.commit()
        db.refresh(relacao)
        return relacao
    return None


def delete_link_product_user(db: Session, id: int):
    """
    Deleta uma relação entre usuário e produto do banco de dados.

    Args:
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.
        id (int): ID da relação entre usuário e produto que deseja-se remover.

    Returns:
        int: Retorna o número de linhas afetadas pela operação de deleção. Deve ser 1 se a deleção for bem-sucedida.
    """
    flag = db.query(models.IntermediariaUserProducts).filter(models.IntermediariaUserProducts.id == id).delete()
    db.commit()
    return flag
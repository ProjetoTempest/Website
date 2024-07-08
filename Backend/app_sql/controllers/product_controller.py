from sqlalchemy.orm import Session, joinedload
from .. import schemas, models

import json


def create_product(db: Session, product: dict):
    """
    Cria um novo produto no banco de dados com base nos dados fornecidos.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - product (dict): Um dicionário contendo os dados do produto a ser criado.
      Deve conter as chaves "title", "description", "value" e "images".

    Returns:
    - models.Products: O objeto do produto criado no banco de dados, incluindo as imagens associadas.
    """
    dicPro = {
        "title": product["title"],
        "description": product["description"],
        "value": product["value"]
    }

    # Crie a instância do produto
    db_product = models.Products(**dicPro)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    id_product = db_product.id

    # Crie e adicione as instâncias de imagens associadas ao produto
    list_imgs = []
    for img in product["images"]:
        img_schema = models.ImagesProducts(
            title=img,
            path=img,
            products_id=id_product
        )
        db.add(img_schema)
        list_imgs.append(img_schema)

    db.commit()

    # Atualize o produto com as imagens associadas
    db_product.images = list_imgs
    db.commit()
    db.refresh(db_product)

    return db_product



def get_products(db: Session):
    """
    Retorna todos os produtos do banco de dados.

    Args:
    - db (Session): A sessão do banco de dados para executar a consulta.

    Returns:
    - List[Products]: Uma lista de todos os produtos no banco de dados, cada produto
      opcionalmente carregado com suas imagens associadas.
    """
    return db.query(models.Products).options(joinedload(models.Products.images)).all()

def get_product(db: Session, product_id: int):
    """
    Retorna um produto com base no ID fornecido.

    Args:
        db (Session): A sessão do banco de dados.
        user_id (int): O ID do produto.

    Returns:
        models.Products | None: O produto encontrado ou None se nenhum produto corresponder ao ID fornecido.
    """
    return db.query(models.Products).filter(models.Products.id == product_id).options(joinedload(models.Products.images)).first()


def update_product(db: Session, db_product: models.Products, product_update: schemas.ProductUpdate):
    """
    Atualiza um produto existente no banco de dados com base nos dados fornecidos.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - db_product (models.Products): O produto no banco de dados que será atualizado.
    - product_update (schemas.ProductUpdate): Os dados atualizados do produto.

    Returns:
    - models.Products: O objeto do produto atualizado no banco de dados.
    """
    update_data = product_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        match key:
            case "title":
                db_product.title = value
            case "description":
                db_product.description = value
            case "value":
                db_product.value = value

    db.commit()
    db.refresh(db_product)
    return db_product



def delete_product(db: Session, product_id: int):
    """
    Remove um produto do banco de dados com base no ID fornecido.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - product_id (int): O ID do produto que deve ser removido.

    Returns:
    - int: O número de registros afetados pela operação de exclusão.
      Retorna 1 se o produto foi encontrado e removido com sucesso,
      ou 0 se nenhum produto correspondente ao ID foi encontrado.
    """
    flag = db.query(models.Products).filter(models.Products.id == product_id).delete()
    db.commit()

    return flag
from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, HTTPException
from typing import Annotated, List

from fastapi.responses import FileResponse
from pathlib import Path
from typing import Annotated
from fastapi import File, Form, UploadFile

import os
import shutil
import json


from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, models
from ..controllers import user_link_products_controller, product_controller, user_controller


route_user_link_products = APIRouter(prefix="/user_link_products")


@route_user_link_products.post("/create_link_product_user/{product_id}/{user_id}")
def create_link_product_user(product_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Cria um link entre um produto e um usuário.

    Args:
        product_id (int): ID do produto.
        user_id (int): ID do usuário.
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        dict: Mensagem indicando que o link foi criado com sucesso.

    Raises:
        HTTPException: Se o usuário ou o produto não forem encontrados, retorna status code 404.
        HTTPException: Se o link já tiver sido criado anteriormente, retorna status code 400.
    """
    prod = product_controller.get_product(db=db, product_id=product_id)
    user = user_controller.get_user(db=db, user_id=user_id)

    if user is None or prod is None:
        raise HTTPException(status_code=404, detail="User or Product not found")
    if user_link_products_controller.get_relacao_product_user_create(db=db, id_user=user_id, id_product=product_id) is not None:
        raise HTTPException(status_code=400, detail="Link already created")

    user_link_products_controller.create_link_product_user(db=db, product_id=product_id, user_id=user_id)
    return {"message": "Link created successfully"}

@route_user_link_products.get("/get_relacao_product_user/")
def get_all_relacao_product_user(db: Session = Depends(get_db)):
    """
    Retorna todas as relações entre usuários e produtos no banco de dados.

    Args:
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        List[models.IntermediariaUserProducts]: Lista de objetos representando todas as relações entre usuários e produtos.
    """
    relacao = user_link_products_controller.get_all_relacao_product_user(db=db)
    return relacao

@route_user_link_products.get("/get_relacao_product_user/{id_relacao}", response_model=schemas.IntermediariaUserProducts)
def get_relacao_product_user_id(id_relacao: int, db: Session = Depends(get_db)):
    """
    Retorna a relação entre usuário e produto com base no ID da relação.

    Args:
        id_relacao (int): ID da relação entre usuário e produto.
        db (Session, opcional): Sessão do banco de dados. Obtido automaticamente por dependência.

    Returns:
        schemas.IntermediariaUserProducts: Objeto representando a relação entre usuário e produto com o ID especificado.

    Raises:
        HTTPException: Se a relação não for encontrada, retorna status code 404.
    """
    relacao = user_link_products_controller.get_relacao_product_user_id(db=db, id=id_relacao)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Relacao not found")
    return relacao

@route_user_link_products.get("/get_products_by_user/{user_id}", response_model=list[schemas.ProductBase])
def get_products_user(user_id: int, db: Session = Depends(get_db)):
    """
    Essa rota retorna todos os produtos associados a um usuário específico.

    Args:
        user_id (int): ID do usuário para o qual deseja-se recuperar os produtos.
        db (Session, optional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.ProductBase]: Uma lista de objetos do tipo `ProductBase` que representam os produtos associados ao usuário.

    Raises:
        HTTPException: Se o usuário não for encontrado (status_code 404).
    """
    user = user_controller.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    products = user_link_products_controller.get_products_by_user(db=db, user_id=user.id)
    return products

@route_user_link_products.get("/get_user_by_product/{product_id}", response_model=list[schemas.UserBase])
def get_user_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retorna todos os usuários associados a um produto específico.

    Args:
        product_id (int): ID do produto para o qual deseja-se recuperar os usuários.
        db (Session, optional): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        List[schemas.UserBase]: Uma lista de objetos do tipo `UserBase` que representam os usuários associados ao produto.

    Raises:
        HTTPException: Se o produto não for encontrado (status_code 404).
    """
    product = product_controller.get_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return user_link_products_controller.get_user_by_product(db=db, product_id=product.id)

@route_user_link_products.put("/update_userid_link_product/{id_relacao}/{user_id}", response_model=schemas.IntermediariaUserProducts)
def update_userid_link_product(id_relacao:int, user_id:int, db: Session = Depends(get_db)):
    """
    Atualiza o ID do usuário em uma relação entre usuário e produto específica.

    Args:
        id_relacao (int): ID da relação entre usuário e produto que deseja-se atualizar.
        user_id (int): Novo ID do usuário para atualização na relação.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        schemas.IntermediariaUserProducts: Objeto que representa a relação usuário-produto atualizada.

    Raises:
        HTTPException: Se o usuário não for encontrado com o ID especificado.
        HTTPException: Se a relação entre usuário e produto não for encontrada com o ID especificado.
    """
    user = user_controller.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    relacao = user_link_products_controller.update_userid_link_product(db=db, id_relacao=id_relacao, id_user=user_id)

    if relacao is None:
        raise HTTPException(status_code=404, detail="Relacao not found")
    return relacao

@route_user_link_products.put("/update_produtid_link_user/{id_relacao}/{produt_id}", response_model=schemas.IntermediariaUserProducts)
def update_produtid_link_user(id_relacao:int, produt_id:int, db: Session = Depends(get_db)):
    """
    Atualiza o ID do produto em uma relação entre usuário e produto específica.

    Args:
        id_relacao (int): ID da relação entre usuário e produto que deseja-se atualizar.
        product_id (int): Novo ID do produto para atualização na relação.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        schemas.IntermediariaUserProducts: Objeto que representa a relação usuário-produto atualizada.

    Raises:
        HTTPException: Se o produto não for encontrado com o ID especificado.
        HTTPException: Se a relação entre usuário e produto não for encontrada com o ID especificado.
    """
    product = product_controller.get_product(db=db, product_id=produt_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    relacao = user_link_products_controller.update_produtid_link_user(db=db, id_relacao=id_relacao, id_produt=produt_id)
    if relacao is None:
        raise HTTPException(status_code=404, detail="Relacao not found")
    return relacao

@route_user_link_products.delete("/delete_link_product_user/{id_relacao}")
def delete_link_product_user(id_relacao: int, db: Session = Depends(get_db)):
    """
    Endpoint para deletar uma relação entre usuário e produto do banco de dados.

    Args:
        id_relacao (int): ID da relação entre usuário e produto que deseja-se remover.
        db (Session): Sessão do banco de dados SQLAlchemy. Obtida através da dependência `get_db`.

    Returns:
        dict: Um dicionário contendo uma mensagem de sucesso e o status HTTP 200 se a relação foi removida com sucesso.

    Raises:
        HTTPException: Retorna um erro 404 se a relação não for encontrada no banco de dados.
    """
    relacao = user_link_products_controller.delete_link_product_user(db=db, id=id_relacao)
    if relacao == 0:
        raise HTTPException(status_code=404, detail="Relacao not found")
    return {"message": "Relacão deleted successfully", "status": 200}
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
from ..controllers import product_controller


routerProduct = APIRouter(prefix="/products")

async def save_images(images: list[UploadFile], product: str):

    path = "/home/will/Documentos/project_tempest/Website/Backend/imagens/"
    if not os.path.exists(path):
        os.makedirs(path)

    listPath = []
    for img in images:
        extension = os.path.splitext(img.filename) [-1]
        temp_file_name = os.path.join(path, product + img.filename)


        listPath.append(temp_file_name)
        with open(temp_file_name, "wb") as buffer:
            shutil.copyfileobj (img.file, buffer)

    return listPath



@routerProduct.post("/", response_model=schemas.Product) 
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Rota para criar um novo produto no banco de dados.

    Args:
    - title (str): Título do produto.
    - description (str): Descrição do produto.
    - value (float): Valor do produto.
    - images (List[UploadFile]): Lista de arquivos de imagem a serem associados ao produto.
    - db (Session): Sessão do banco de dados para executar a operação de criação.

    Returns:
    - models.Products: Objeto do produto criado no banco de dados.
    """

    return product_controller.create_product(db=db, product=product)




@routerProduct.get("/")
def read_products(db: Session = Depends(get_db)):
    """
    Rota para buscar todos os produtos no banco de dados.

    Args:
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - List[models.Products]: Lista de todos os produtos presentes no banco de dados.
    """
    return product_controller.get_products(db)


@routerProduct.get("/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar um produto específico no banco de dados pelo seu ID.

    Args:
    - product_id (int): O ID do produto que se deseja buscar.
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - models.Products: Objeto do produto encontrado no banco de dados.

    Raises:
    - HTTPException(404): Retorna um erro 404 se o produto não for encontrado no banco de dados.
    """
    product = product_controller.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@routerProduct.put("/update/{product_id}", response_model=schemas.ProductBase)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """
    Rota para atualizar um produto específico no banco de dados pelo seu ID.

    Args:
    - product_id (int): O ID do produto que se deseja atualizar.
    - product (schemas.ProductUpdate): Dados atualizados do produto a serem aplicados.
    - db (Session): Sessão do banco de dados para executar a operação de atualização.

    Returns:
    - schemas.ProductBase: Dados do produto atualizado, conforme definido no esquema `schemas.ProductBase`.

    Raises:
    - HTTPException(404): Retorna um erro 404 se o produto não for encontrado no banco de dados.
    """
    db_product = product_controller.get_product(db=db, product_id=product_id)
    if db_product:
        return product_controller.update_product(db=db, db_product=db_product, product_update=product)    
    raise HTTPException(status_code=404, detail="Product not found")


@routerProduct.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Rota para excluir um produto específico do banco de dados pelo seu ID.

    Args:
    - product_id (int): O ID do produto que se deseja excluir.
    - db (Session): Sessão do banco de dados para executar a operação de exclusão.

    Returns:
    - dict: Um dicionário com uma mensagem de sucesso e um status code 200 indicando que o produto foi excluído com sucesso.

    Raises:
    - HTTPException(404): Retorna um erro 404 se o produto não for encontrado no banco de dados.
    """
    flag = product_controller.delete_product(db=db, product_id=product_id)
    if flag == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully", "status": 200}








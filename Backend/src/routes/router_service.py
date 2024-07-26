from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List, Optional

from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, models
from ..controllers import service_controller  

import os
import shutil

routerService = APIRouter(prefix="/services")

async def save_images(images: List[UploadFile], service: str):
    """
    Função auxiliar para salvar imagens no diretório especificado.

    Args:
    - images (List[UploadFile]): Lista de arquivos de imagem a serem salvos.
    - service (str): Nome do serviço para criar o nome do arquivo.

    Returns:
    - List[str]: Lista de caminhos dos arquivos salvos.
    """
    path = "/home/will/Documentos/project_tempest/Website/Backend/imagens/"
    if not os.path.exists(path):
        os.makedirs(path)

    saved_image_urls = []
    for img in images:
        extension = os.path.splitext(img.filename)[-1]
        temp_file_name = os.path.join(path, service + img.filename)

        saved_image_urls.append(temp_file_name)
        with open(temp_file_name, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return saved_image_urls


@routerService.post("/")
async def create_service(
    title: str = Form(...),
    description: str = Form(...),
    value: float = Form(...),
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    """
    Rota para criar um novo serviço no banco de dados.

    Args:
    - title (str): Título do serviço.
    - description (str): Descrição do serviço.
    - value (float): Valor do serviço.
    - images (List[UploadFile]): Lista de arquivos de imagem a serem associados ao serviço.
    - db (Session): Sessão do banco de dados para executar a operação de criação.

    Returns:
    - models.Services: Objeto do serviço criado no banco de dados.
    """
    service_dict = {
        "title": title,
        "description": description,
        "value": value,
        "images": None,
    }

    if images:
        saved_image_urls = await save_images(images, title)
        service_dict['images'] = saved_image_urls

    return service_controller.create_service(db=db, service=service_dict)

@routerService.post("/serv", response_model=schemas.ServiceResponse)
async def create_service( servico: schemas.ServiceCreate,
    db: Session = Depends(get_db)
):
    """
    Rota para criar um novo serviço no banco de dados.

    Args:
    - title (str): Título do serviço.
    - description (str): Descrição do serviço.
    - value (float): Valor do serviço.
    - images (List[UploadFile]): Lista de arquivos de imagem a serem associados ao serviço.
    - db (Session): Sessão do banco de dados para executar a operação de criação.

    Returns:
    - models.Services: Objeto do serviço criado no banco de dados.
    """
    
    return service_controller.create_service(db=db, service=servico)


@routerService.get("/")
def read_services(db: Session = Depends(get_db)):
    """
    Rota para buscar todos os serviços no banco de dados.

    Args:
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - List[models.Services]: Lista de todos os serviços presentes no banco de dados.
    """
    return service_controller.get_services(db)

@routerService.get("/{service_id}")
def read_service(service_id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar um serviço específico no banco de dados pelo seu ID.

    Args:
    - service_id (int): O ID do serviço que se deseja buscar.
    - db (Session): Sessão do banco de dados para executar a operação de busca.

    Returns:
    - models.Services: Objeto do serviço encontrado no banco de dados.

    Raises:
    - HTTPException(404): Retorna um erro 404 se o serviço não for encontrado no banco de dados.
    """
    service = service_controller.get_service(db=db, service_id=service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@routerService.put("/update/{service_id}", response_model=schemas.ServiceBase)
def update_service(service_id: int, service: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    """
    Rota para atualizar um serviço específico no banco de dados pelo seu ID.

    Args:
    - service_id (int): O ID do serviço que se deseja atualizar.
    - service (schemas.ServiceUpdate): Dados atualizados do serviço a serem aplicados.
    - db (Session): Sessão do banco de dados para executar a operação de atualização.

    Returns:
    - schemas.ServiceBase: Dados do serviço atualizado, conforme definido no esquema `schemas.ServiceBase`.

    Raises:
    - HTTPException(404): Retorna um erro 404 se o serviço não for encontrado no banco de dados.
    """
    db_service = service_controller.get_service(db=db, service_id=service_id)
    if db_service:
        return service_controller.update_service(db=db, db_service=db_service, service_update=service)    
    raise HTTPException(status_code=404, detail="Service not found")

@routerService.delete("/delete/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    """
    Rota para excluir um serviço específico do banco de dados pelo seu ID.

    Args:
    - service_id (int): O ID do serviço que se deseja excluir.
    - db (Session): Sessão do banco de dados para executar a operação de exclusão.

    Returns:
    - dict: Um dicionário com uma mensagem de sucesso e um status code 200 indicando que o serviço foi excluído com sucesso.

    Raises:
    - HTTPException(404): Retorna um erro 404 se o serviço não for encontrado no banco de dados.
    """
    flag = service_controller.delete_service(db=db, service_id=service_id)
    if flag == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully", "status": 200}

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



from .database import get_db
from sqlmodel import Session

from . import schemas, crud2, models #hash_password

# routerUser = APIRouter(prefix="/users")
# routerProduct = APIRouter(prefix="/products")
# routerService = APIRouter(prefix="/service")

# # imageas bit

# def safe_file_to_server(uploaded_file, name_user):
#     path = "/home/will/Documentos/project_tempest/Website/Backend/imagens/"
#     if not os.path.exists(path):
#         os.makedirs(path)

#     extension = os.path.splitext(uploaded_file.filename) [-1]
#     temp_file_name = os.path.join(path, name_user + extension)

#     with open(temp_file_name, "wb") as buffer:
#         shutil.copyfileobj (uploaded_file.file, buffer)
#     return temp_file_name


# #Users

# """
#     Rota para criar um user

#     Args:
#         user (models.UserCreate): Dados do user.
#         db (Session): Cria e gerencia transações do banco de dados.

#     Returns:
#         models.UserBase: A soma de a e b.
# """
# @routerUser.post("/", response_model= schemas.UserBase)
# async def create_user(
#     user: schemas.UserCreate,
#     db: Session = Depends(get_db)
# ):
#     """
#     Cria um novo usuário na aplicação.

#     Este endpoint recebe os dados do usuário e cria um novo registro no banco de dados.
#     Se o email já estiver registrado, retorna um erro 400.

#     Args:
#         user (models.UserCreate): Um objeto que contém os dados do usuário a ser criado.
#         db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

#     Returns:
#         models.UserBase: Um objeto que representa o usuário criado, sem a senha.

#     Raises:
#         HTTPException: Se o email já estiver registrado, retorna uma exceção HTTP 400.
#     """

#     db_user = crud2.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     return crud2.create_user(db=db, user=user) 

# @routerUser.get("/{user_id}", response_model= schemas.UserBase)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     """
#     Obtém um usuário pelo ID.

#     Este endpoint recebe um ID de usuário e retorna os detalhes do usuário correspondente.
#     Se o usuário não for encontrado, retorna um erro 404.

#     Args:
#         user_id (int): O ID do usuário a ser recuperado.
#         db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

#     Returns:
#         schemas.UserBase: Um objeto que representa os detalhes do usuário.

#     Raises:
#         HTTPException: Se o usuário não for encontrado, retorna uma exceção HTTP 404.
#     """
#     db_user = crud2.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user



# @routerUser.get("/login/{email}/{senha}", response_model=schemas.UserBase)
# def login_user(email: str, senha: str, db: Session = Depends(get_db)):
#     """
#     Autentica um usuário pelo email e senha.

#     Este endpoint recebe um email e uma senha e retorna os detalhes do usuário correspondente,
#     caso a autenticação seja bem-sucedida. Se o usuário não for encontrado, retorna um erro 404.

#     Args:
#         email (str): O email do usuário a ser autenticado.
#         senha (str): A senha do usuário a ser autenticado.
#         db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

#     Returns:
#         schemas.UserBase: Um objeto que representa os detalhes do usuário autenticado.

#     Raises:
#         HTTPException: Se o usuário não for encontrado, retorna uma exceção HTTP 404.
#     """
#     db_user = crud2.get_user_by_email_password(db, email=email, password=senha)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @routerUser.get("/", response_model=list[schemas.UserBase])
# def read_users(db: Session = Depends(get_db)):
#     """
#     Obtém todos os usuários.

#     Este endpoint retorna uma lista com todos os usuários registrados no banco de dados.

#     Args:
#         db (Session): Uma sessão do banco de dados injetada automaticamente pelo FastAPI.

#     Returns:
#         list[schemas.UserBase]: Uma lista de objetos que representam os usuários registrados.
#     """
#     users = crud2.get_users(db)
#     return users

# @routerUser.put("/upadate_email/{new_email}/{old_email}", response_model= schemas.UserBase)
# def update_email(new_email: str, old_email: str, db: Session = Depends(get_db)):
#     """
#     Atualiza o e-mail de um usuário.

#     Este endpoint atualiza o e-mail de um usuário existente. Se o usuário com o e-mail antigo não for encontrado, retorna um erro 404.

#     Args:
#         old_email (str): O e-mail antigo do usuário.
#         new_email (str): O novo e-mail do usuário.
#         db (Session): A sessão do banco de dados injetada automaticamente pelo FastAPI.

#     Returns:
#         schemas.UserBase: Os dados do usuário atualizado.
#     """

#     updated_user = crud2.update_email_user(db=db, new_email=new_email, old_email=old_email)

#     if updated_user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     return updated_user


# @routerUser.put("/update_user/{user_id}", response_model=schemas.UserBase)
# def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
#     """
#     Atualiza os dados de um usuário.

#     Este endpoint atualiza os dados de um usuário existente. Apenas os campos fornecidos (não `None`)
#     serão atualizados. Se o usuário não for encontrado, retorna um erro 404.

#     Args:
#         user_id (int): O ID do usuário a ser atualizado.
#         user_update (schemas.UserUpdate): Os dados atualizados do usuário.
#         db (Session): A sessão do banco de dados injetada automaticamente pelo FastAPI.

#     Returns:
#         schemas.UserBase: Os dados do usuário atualizado.
#     """
#     db_user = crud2.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     print(db_user)

#     updated_user = crud2.update_user_fields(db=db, db_user=db_user, user_update=user_update)

#     return updated_user



# # @routerUser.put("/update")
# # def update_user_info_all(user: schemas.UserCreate, db: Session = Depends(get_db)):
# #     pass

# @routerUser.delete("/delete/{email}/{password}")
# def delete_user(email: str, password: str, db: Session = Depends(get_db)):
#     """
#     Deleta um usuário com base no email e senha fornecidos.

#     Args:
#         email (str): O email do usuário a ser deletado.
#         password (str): A senha do usuário a ser deletado.
#         db (Session): A sessão do banco de dados, fornecida automaticamente pelo FastAPI.

#     Raises:
#         HTTPException: Se o usuário não for encontrado ou a senha estiver incorreta, retorna uma exceção HTTP 400 com a mensagem "User not found or incorrect password".

#     Returns:
#         dict: Um dicionário com uma mensagem de sucesso e o status HTTP 200.
#     """
#     deleted_count = crud2.delete_user_by_email_password(db=db, email=email, password=password)

#     if deleted_count == 0:
#         raise HTTPException(status_code=400, detail="User not found or incorrect password")
#     return {"message": "User deleted successfully", "status": 200}


































# ##############################################

# async def save_images(images: list[UploadFile], product: str):

#     path = "/home/will/Documentos/project_tempest/Website/Backend/imagens/"
#     if not os.path.exists(path):
#         os.makedirs(path)

#     listPath = []
#     for img in images:
#         extension = os.path.splitext(img.filename) [-1]
#         temp_file_name = os.path.join(path, product + img.filename)


#         listPath.append(temp_file_name)
#         with open(temp_file_name, "wb") as buffer:
#             shutil.copyfileobj (img.file, buffer)

#     return listPath



# @routerProduct.post("/")  #response_model=schemas.Products
# async def create_product(title: Annotated[str, Form()], description: Annotated[str, Form()], value: Annotated[float, Form()], images: Annotated[List[UploadFile], File(description="Multiple files as UploadFile")], db: Session = Depends(get_db)):



#     product_dict = {
#         "title": title,
#         "description": description,
#         "value": value,
#         "images": images,
#     }

    
#     saved_image_urls = await save_images(images, title)
#     product_dict['images'] = saved_image_urls

#     a = crud.create_product(db=db, product=product_dict)

#     print(a)

#     return a


# @routerProduct.get("/", response_model=list[schemas.Products])
# def read_products(db: Session = Depends(get_db)):
#     products = crud.get_products(db)
#     return products

# @routerProduct.get("/{product_id}", response_model=schemas.Products)
# def read_product(product_id: int, db: Session = Depends(get_db)):
#     product = crud.get_product(db, product_id=product_id)
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

# @routerProduct.put("/update/{product_id}", response_model=schemas.Products)
# def update_product(product_id: int, product: schemas.Products, db: Session = Depends(get_db)):
#     db_product = crud.update_product(db=db, product_id=product_id, product=product)
#     # if db_product is None:
#         # raise HTTPException(status_code=404, detail="Product not found")
#     # return db_product

# @routerProduct.delete("/delete/{product_id}", response_model=schemas.Products)
# def delete_product(product_id: int, db: Session = Depends(get_db)):
#     db_product = crud.delete_product(db=db, product_id=product_id)
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return db_product


























# @routerProduct.post("/create_link_product_user/{product_id}/{user_id}")
# def create_link_product_user(product_id: int, user_id: int, db: Session = Depends(get_db)):
#     prod = crud.get_product(db=db, product_id=product_id)
#     user = crud.get_user(db=db, user_id=user_id)

#     if user is None or prod is None:
#         raise HTTPException(status_code=404, detail="User or Product not found")
#     if crud.get_relacao_product_user_create(db=db, id_user=user_id, id_product=product_id) is not None:
#         raise HTTPException(status_code=400, detail="Link already created")

#     crud.create_link_product_user(db=db, product_id=product_id, user_id=user_id)
#     return {"message": "Link created successfully"}

# @routerProduct.get("/get_relacao_product_user/")
# def get_relacao_product_user(db: Session = Depends(get_db)):
#     # print("passou aqui route")
#     relacao = crud.get_relacao_product_user(db=db)
#     # print("passou aqui route2")
#     return relacao

# @routerProduct.get("/get_relacao_product_user/{id_relacao}", response_model=schemas.IntermediariaUserProducts)
# def get_relacao_product_user_id(id_relacao: int, db: Session = Depends(get_db)):
#     relacao = crud.get_relacao_product_user_id(db=db, id=id_relacao)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao

# @routerProduct.get("/get_products_by_user/{user_id}", response_model=list[schemas.Products])
# def get_products_user(user_id: int, db: Session = Depends(get_db)):
#     user = crud.get_user(db=db, user_id=user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     products = crud.get_products_by_user(db=db, user_id=user.id)
#     return products

# @routerProduct.get("/get_user_by_product/{product_id}", response_model=list[schemas.User])
# def get_user_product(product_id: int, db: Session = Depends(get_db)):
#     product = crud.get_product(db=db, product_id=product_id)
#     if product is None:
#         raise HTTPException(status_code=404, detail="product not found")
#     users = crud.get_user_by_product(db=db, product_id=product.id)

#     return users

# @routerProduct.put("/update_userid_link_product/{id_relacao}/{user_id}", response_model=schemas.IntermediariaUserProducts)
# def update_userid_link_product(id_relacao:int, user_id:int, db: Session = Depends(get_db)):
#     relacao = crud.update_userid_link_product(db=db, id_relacao=id_relacao, id_user=user_id)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao

# @routerProduct.put("/update_produtid_link_user/{id_relacao}/{produt_id}", response_model=schemas.IntermediariaUserProducts)
# def update_produtid_link_user(id_relacao:int, produt_id:int, db: Session = Depends(get_db)):
#     relacao = crud.update_produtid_link_user(db=db, id_relacao=id_relacao, id_produt=produt_id)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao

# @routerProduct.delete("/delete_link_product_user/{id_relacao}", response_model=schemas.IntermediariaUserProducts)
# def delete_link_product_user(id_relacao: int, db: Session = Depends(get_db)):
#     relacao = crud.delete_link_product_user(db=db, id=id_relacao)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao
























# # ##############################################


# @routerService.post("/", response_model=schemas.Service)
# def create_service(service: schemas.Service, db: Session = Depends(get_db)):
#     return crud.create_service(db=db, service=service)

# @routerService.get("/", response_model=list[schemas.Service])
# def read_services(db: Session = Depends(get_db)):
#     services = crud.get_services(db)
#     return services

# @routerService.get("/{service_id}", response_model=schemas.Service)
# def read_service(service_id: int, db: Session = Depends(get_db)):
#     service = crud.get_service(db, service_id=service_id)
#     if service is None:
#         raise HTTPException(status_code=404, detail="Service not found")
#     return service

# @routerService.put("/update/{service_id}", response_model=schemas.Service)
# def update_service(service_id: int, service: schemas.Service, db: Session = Depends(get_db)):
#     db_service = crud.update_service(db=db, service_id=service_id, service=service)
#     # if db_service is None:
#         # raise HTTPException(status_code=404, detail="Service not found")
#     # return db_service

# @routerService.delete("/delete/{service_id}", response_model=schemas.Service)
# def delete_service(service_id: int, db: Session = Depends(get_db)):
#     db_service = crud.delete_service(db=db, service_id=service_id)
#     if db_service is None:
#         raise HTTPException(status_code=404, detail="Service not found")
#     return db_service





















# @routerService.post("/create_link_service_user/{service_id}/{user_id}")
# def create_link_service_user(service_id: int, user_id: int, db: Session = Depends(get_db)):
#     serv = crud.get_service(db=db, service_id=service_id)
#     user = crud.get_user(db=db, user_id=user_id)

#     if user is None or serv is None:
#         raise HTTPException(status_code=404, detail="User or Service not found")
#     if crud.get_relacao_service_user_create(db=db, id_user=user_id, id_service=service_id) is not None:
#         raise HTTPException(status_code=400, detail="Link already created")

#     crud.create_link_service_user(db=db, service_id=service_id, user_id=user_id)
#     return {"message": "Link created successfully"}

# @routerService.get("/get_relacao_service_user/")
# def get_relacao_service_user(db: Session = Depends(get_db)):
#     # print("passou aqui route")
#     relacao = crud.get_relacao_service_user(db=db)
#     # print("passou aqui route2")
#     return relacao

# @routerService.get("/get_relacao_service_user/{id_relacao}", response_model=schemas.IntermediariaUserServices)
# def get_relacao_service_user_id(id_relacao: int, db: Session = Depends(get_db)):
#     relacao = crud.get_relacao_service_user_id(db=db, id=id_relacao)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao

# @routerService.get("/get_services_by_user/{user_id}", response_model=list[schemas.Service])
# def get_services_user(user_id: int, db: Session = Depends(get_db)):
#     user = crud.get_user(db=db, user_id=user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     services = crud.get_services_by_user(db=db, user_id=user.id)
#     return services

# @routerService.get("/get_user_by_service/{service_id}", response_model=list[schemas.User])
# def get_user_service(service_id: int, db: Session = Depends(get_db)):
#     service = crud.get_service(db=db, service_id=service_id)
#     if service is None:
#         raise HTTPException(status_code=404, detail="Service not found")
#     users = crud.get_user_by_service(db=db, service_id=service.id)

#     return users

# @routerService.put("/update_userid_link_service/{id_relacao}/{user_id}", response_model=schemas.IntermediariaUserServices)
# def update_userid_link_service(id_relacao:int, user_id:int, db: Session = Depends(get_db)):
#     relacao = crud.update_userid_link_service(db=db, id_relacao=id_relacao, id_user=user_id)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao

# @routerService.put("/update_serviceid_link_user/{id_relacao}/{service_id}", response_model=schemas.IntermediariaUserServices)
# def update_serviceid_link_user(id_relacao:int, service_id:int, db: Session = Depends(get_db)):
#     relacao = crud.update_serviceid_link_user(db=db, id_relacao=id_relacao, id_service=service_id)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao

# @routerService.delete("/delete_link_service_user/{id_relacao}", response_model=schemas.IntermediariaUserServices)
# def delete_link_service_user(id_relacao: int, db: Session = Depends(get_db)):
#     relacao = crud.delete_link_service_user(db=db, id=id_relacao)
#     if relacao is None:
#         raise HTTPException(status_code=404, detail="Relacao not found")
#     return relacao

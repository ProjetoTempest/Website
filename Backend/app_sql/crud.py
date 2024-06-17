# from sqlalchemy.orm import Session
from sqlmodel import Session, select, delete, update, join
from . import schemas

import json


def get_user(db: Session, user_id: int):
    query = select(schemas.User).where(schemas.User.id == user_id)
    user_db = db.exec(query).first()
    return user_db

def get_user_by_email(db: Session, email: str):
    query = select(schemas.User).where(schemas.User.email == email)
    return db.exec(query).first()

def get_user_by_email_password(db: Session, email: str, password: str):
    query = select(schemas.User).where(schemas.User.email == email, schemas.User.password == password)
    user_db = db.exec(query).first()
    return user_db

def get_users(db: Session, skip: int = 0, limit: int = 100):
    query = select(schemas.User).offset(skip).limit(limit)
    users_db = db.exec(query)
    return users_db

def create_user(db: Session, user: json):
    print("Crud")
    db_user = schemas.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Colocar senha para verificação
def update_email_user(db: Session, new_email:str, old_email):
    query = update(schemas.User).where(schemas.User.email == old_email).values(email=new_email)
    user_db = db.exec(query)
    # db.add(user_db)
    db.commit()
    # db.refresh(user_db)
    return user_db

def update_all_infos_user(db: Session, user:schemas.User):
    pass


def delete_user_by_email_password(db: Session, email: str, password: str):
    user_db = get_user_by_email_password(db=db, email=email, password=password)
    if user_db is None:
        return None
    query = delete(schemas.User).where(schemas.User.email == email, schemas.User.password == password)
    db.exec(query)
    db.commit()
    return user_db



 ############################### Products



def create_product(db: Session, product: dict):
    dicPro = {
        "title": product["title"],
        "description": product["description"],
        "value": product["value"]
    }

    # Crie a instância do produto
    db_product = schemas.Products(**dicPro)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    id_product = db_product.id

    # Crie e adicione as instâncias de imagens associadas ao produto
    list_imgs = []
    for img in product["images"]:
        img_schema = schemas.ImagesProducts(
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



from sqlalchemy.orm import joinedload


def get_products(db: Session):
    query = (
        select(schemas.Products)
        .options(joinedload(schemas.Products.images))
    )
    products_db = db.exec(query).unique().all()
    return products_db

# def get_products(db: Session):
#     query = (
#         select(schemas.Products)
#         .options(joinedload(schemas.Products.images))
#     )
#     products_db = db.exec(query).all()

#     return products_db

# def get_products(db: Session):
#     query = select(schemas.Products)
#     products_db = db.exec(query)
#     return products_db

def get_product(db: Session, product_id: int):
    query = select(schemas.Products).where(schemas.Products.id == product_id)
    product_db = db.exec(query).first()
    return product_db

def update_product(db: Session, product_id: int, product: schemas.Products):
    query = update(schemas.Products).where(schemas.Products.id == product_id).values(title=product.title, description=product.description, value=product.value)
    db.exec(query)
    db.commit()
    # return product_db

def delete_product(db: Session, product_id: int):
    product_db = get_product(db=db, product_id=product_id)

    if product_db is not None:
        query = delete(schemas.Products).where(schemas.Products.id == product_id)
        db.exec(query)
        db.commit()

    return product_db

def create_link_product_user(db: Session, product_id: int, user_id: int):
    db_product_user = schemas.IntermediariaUserProducts(user_id=user_id, products_id=product_id)
    db.add(db_product_user)
    db.commit()
    db.refresh(db_product_user)

    return db_product_user

def update_userid_link_product(db: Session, id_relacao: int, id_user: int):
    query = update(schemas.IntermediariaUserProducts).where(schemas.IntermediariaUserProducts.id == id_relacao).values(user_id=id_user)
    db.exec(query)
    db.commit()

    query = select(schemas.IntermediariaUserProducts).where(schemas.IntermediariaUserProducts.id == id_relacao)
    relacao_Product_User = db.exec(query).first()

    return relacao_Product_User

def update_produtid_link_user(db: Session, id_relacao: int, id_produt: int):
    query = update(schemas.IntermediariaUserProducts).where(schemas.IntermediariaUserProducts.id == id_relacao).values(products_id=id_produt)
    db.exec(query)
    db.commit()

    query = select(schemas.IntermediariaUserProducts).where(schemas.IntermediariaUserProducts.id == id_relacao)
    relacao_Product_User = db.exec(query).first()

    return relacao_Product_User


def get_relacao_product_user_create(db: Session, id_user: int, id_product: int):
    query = select(schemas.IntermediariaUserProducts).where(schemas.IntermediariaUserProducts.user_id == id_user, schemas.IntermediariaUserProducts.products_id == id_product)
    relacao_Product_User = db.exec(query).first()
    return relacao_Product_User

def get_relacao_product_user(db: Session):
    query = select(schemas.IntermediariaUserProducts)
    relacao_Product_User = db.exec(query).all()
    return relacao_Product_User

def get_relacao_product_user_id(db: Session, id: int):
    query = select(schemas.IntermediariaUserProducts).where(schemas.IntermediariaUserProducts.id == id)
    relacao_Product_User = db.exec(query).first()
    return relacao_Product_User

def get_products_by_user(db: Session, user_id: int):
    query = select(schemas.Products).join(schemas.IntermediariaUserProducts, schemas.Products.id == schemas.IntermediariaUserProducts.products_id).where(schemas.IntermediariaUserProducts.user_id == user_id)
    relacao_Product_User = db.exec(query).all()
    return relacao_Product_User
    

def get_user_by_product(db: Session, product_id: int):
    query = select(schemas.User).join(schemas.IntermediariaUserProducts, schemas.User.id == schemas.IntermediariaUserProducts.user_id).where(schemas.IntermediariaUserProducts.products_id == product_id)

    relacao_Product_User = db.exec(query).all()
    return relacao_Product_User

def delete_link_product_user(db: Session, id: int):
    relacao_exist = get_relacao_product_user_id(db=db, id=id)

    if relacao_exist is not None:
        query = delete(schemas.IntermediariaUserProducts).where(schemas.IntermediariaUserProducts.id == id)
        db.exec(query)
        db.commit()

    return relacao_exist


def create_service(db: Session, service: schemas.Service):
    db_service = schemas.Service(title=service.title, description=service.description, value=service.value)
    
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_services(db: Session):
    query = select(schemas.Service)
    services_db = db.exec(query)
    return services_db

def get_service(db: Session, service_id: int):
    query = select(schemas.Service).where(schemas.Service.id == service_id)
    service_db = db.exec(query).first()
    return service_db

def update_service(db: Session, service_id: int, service: schemas.Service):
    query = update(schemas.Service).where(schemas.Service.id == service_id).values(title=service.title, description=service.description, value=service.value)
    db.exec(query)
    db.commit()
    # return service_db

def delete_service(db: Session, service_id: int):
    service_db = get_service(db=db, service_id=service_id)

    if service_db is not None:
        query = delete(schemas.Service).where(schemas.Service.id == service_id)
        db.exec(query)
        db.commit()

    return service_db






def create_link_service_user(db: Session, service_id: int, user_id: int):
    db_service_user = schemas.IntermediariaUserServices(user_id=user_id, service_id=service_id)
    db.add(db_service_user)
    db.commit()
    db.refresh(db_service_user)

    return db_service_user

def update_userid_link_service(db: Session, id_relacao: int, id_user: int):
    query = update(schemas.IntermediariaUserServices).where(schemas.IntermediariaUserServices.id == id_relacao).values(user_id=id_user)
    db.exec(query)
    db.commit()

    query = select(schemas.IntermediariaUserServices).where(schemas.IntermediariaUserServices.id == id_relacao)
    relacao_service_user = db.exec(query).first()

    return relacao_service_user

def update_serviceid_link_user(db: Session, id_relacao: int, id_service: int):
    query = update(schemas.IntermediariaUserServices).where(schemas.IntermediariaUserServices.id == id_relacao).values(service_id=id_service)
    db.exec(query)
    db.commit()

    query = select(schemas.IntermediariaUserServices).where(schemas.IntermediariaUserServices.id == id_relacao)
    relacao_service_user = db.exec(query).first()

    return relacao_service_user


def get_relacao_service_user_create(db: Session, id_user: int, id_service: int):
    query = select(schemas.IntermediariaUserServices).where(schemas.IntermediariaUserServices.user_id == id_user, schemas.IntermediariaUserServices.service_id == id_service)
    relacao_service_user = db.exec(query).first()
    return relacao_service_user

def get_relacao_service_user(db: Session):
    query = select(schemas.IntermediariaUserServices)
    relacao_service_user = db.exec(query).all()
    return relacao_service_user

def get_relacao_service_user_id(db: Session, id: int):
    query = select(schemas.IntermediariaUserServices).where(schemas.IntermediariaUserServices.id == id)
    relacao_service_user = db.exec(query).first()
    return relacao_service_user

def get_services_by_user(db: Session, user_id: int):
    query = select(schemas.Services).join(schemas.IntermediariaUserServices, schemas.Services.id == schemas.IntermediariaUserServices.service_id).where(schemas.IntermediariaUserServices.user_id == user_id)
    relacao_service_user = db.exec(query).all()
    return relacao_service_user
    

def get_user_by_service(db: Session, service_id: int):
    query = select(schemas.User).join(schemas.IntermediariaUserServices, schemas.User.id == schemas.IntermediariaUserServices.user_id).where(schemas.IntermediariaUserServices.service_id == service_id)

    relacao_service_user = db.exec(query).all()
    return relacao_service_user

def delete_link_service_user(db: Session, id: int):
    relacao_exist = get_relacao_service_user_id(db=db, id=id)

    if relacao_exist is not None:
        query = delete(schemas.IntermediariaUserServices).where(schemas.IntermediariaUserServices.id == id)
        db.exec(query)
        db.commit()

    return relacao_exist

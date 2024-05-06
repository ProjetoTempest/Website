# from sqlalchemy.orm import Session
from sqlmodel import Session, select, delete, update
from . import schemas


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


def create_user(db: Session, user: schemas.User):
    db_user = schemas.User(name=user.name, email=user.email, cargotes=user.cargotes, photo=user.photo, description=user.description, password=user.password)
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

def create_product(db: Session, product: schemas.Products):
    db_product = schemas.Products(title=product.title, description=product.description, images=product.images, value=product.value)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    query = select(schemas.Products)
    products_db = db.exec(query)
    return products_db

def get_product(db: Session, product_id: int):
    query = select(schemas.Products).where(schemas.Products.id == product_id)
    product_db = db.exec(query).first()
    return product_db



# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ProductsCreate, user_id: int):
#     db_item = models.Products(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
from fastapi import APIRouter
from fastapi import Depends, HTTPException

from .database import get_db
from sqlmodel import Session

from . import schemas, crud

routerUser = APIRouter(prefix="/users")
routerProduct = APIRouter(prefix="/products")

@routerUser.post("/", response_model=schemas.UserBase)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@routerUser.get("/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@routerUser.get("/login/{email}/{senha}", response_model=schemas.UserBase)
def login_user(email: str, senha: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email_password(db, email=email, password=senha)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@routerUser.get("/", response_model=list[schemas.UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@routerUser.put("/upadate_email/{new_email}/{old_email}", response_model=schemas.UserBase)
def update_email(new_email: str, old_email: str, db: Session = Depends(get_db)):
    user_db = crud.update_email_user(db=db, new_email=new_email, old_email=old_email)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db

@routerUser.put("/update")
def update_user_info_all(user: schemas.User, db: Session = Depends(get_db)):
    pass

@routerUser.delete("/delete/{email}/{password}", response_model= schemas.UserBase)
def delete_user(email:str, password:str, db:Session = Depends(get_db)):
    flag = crud.delete_user_by_email_password(db=db, email=email, password=password)

    if flag is None:
        raise HTTPException(status_code=404, detail="User not found")
    return flag

@routerProduct.post("/", response_model=schemas.Products)
def create_product(product: schemas.Products, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@routerProduct.get("/", response_model=list[schemas.Products])
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@routerProduct.get("/{product_id}", response_model=schemas.Products)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


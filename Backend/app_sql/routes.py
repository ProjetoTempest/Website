from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException

from .database import get_db
from sqlmodel import Session

from . import schemas, crud

routerUser = APIRouter(prefix="/users")

@routerUser.get("/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..controllers import role_controller

route_role = APIRouter(prefix="/roles")

@route_role.post("/create_role")
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return role_controller.create_role(db=db, role=role)

@route_role.get("/{role_id}", response_model=schemas.Role)
def get_role(role_id: int, db: Session = Depends(get_db)):
    db_role = role_controller.get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@route_role.get("/", response_model=list[schemas.Role])
def get_all_roles(db: Session = Depends(get_db)):
    return role_controller.get_all_roles(db=db)

@route_role.put("/{role_id}", response_model=schemas.Role)
def update_role(role_id: int, role_update: schemas.RoleUpdate, db: Session = Depends(get_db)):
    db_role = role_controller.get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_controller.update_role(db=db, db_role=db_role, role_update=role_update)

@route_role.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    flag = role_controller.delete_role(db=db, role_id=role_id)
    if flag == 0:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}

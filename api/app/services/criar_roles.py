# from app.db.connection import get_db
# from app.services.ids import id_generate
# from fastapi import Depends
# from sqlalchemy.orm import Session

# from app.db.models import Role
# from app.schemas.role import RoleRequest

# def criar(db: Session = Depends(get_db)):
#     role = RoleRequest(name='admin', description='Administrador')
#     role = Role(**role.dict(), id=id_generate())
#     db.add(role)
#     db.commit()

# criar(get_db())

from app.db.connection import get_db
from app.services.ids import id_generate
from sqlalchemy.orm import Session
from app.db.models import Role
from app.schemas.role import RoleRequest

def criar(db: Session):
    role = RoleRequest(name='admin', description='Administrador')
    db.add(Role(**role.dict(), id=id_generate()))
    db.commit()

# Executando o script
db = next(get_db())  # Obtendo a sessão de banco de dados
criar(db)  # Passando a sessão para a função criar

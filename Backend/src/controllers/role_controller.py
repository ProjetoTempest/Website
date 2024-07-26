from sqlalchemy.orm import Session
from .. import schemas, models

def create_role(db: Session, role: schemas.RoleBase):
    role = role.model_dump()
    role = models.Role(**role)
    db.add(role)
    db.commit()
    db.refresh(role)

    return role

def get_role(db: Session, role_id: int):
    """
    Retorna um papel (role) com base no ID fornecido.

    Args:
        db (Session): A sessão do banco de dados.
        role_id (int): O ID do papel (role).

    Returns:
        models.Role | None: O papel encontrado ou None se nenhum papel corresponder ao ID fornecido.
    """
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_all_roles(db: Session):
    """
    Retorna todos os papéis (roles) do banco de dados.

    Args:
        db (Session): A sessão do banco de dados.

    Returns:
        List[models.Role] | None: Uma lista de todos os papéis no banco de dados ou None se nenhum papel for encontrado.
    """
    return db.query(models.Role).all()

def update_role(db: Session, db_role: models.Role, role_update: schemas.RoleUpdate):
    """
    Atualiza um papel existente no banco de dados com base nos dados fornecidos.

    Args:
    - db (Session): A sessão do banco de dados para executar a transação.
    - db_role (models.Role): O papel no banco de dados que será atualizado.
    - role_update (schemas.RoleUpdate): Os dados atualizados do papel.

    Returns:
    - models.Role: O objeto do papel atualizado no banco de dados.
    """
    update_data = role_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        match key:
            case "name":
                db_role.title = value
            case "description":
                db_role.description = value

    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    flag = db.query(models.Role).filter(models.Role.id == role_id).delete()
    db.commit()
    return flag

from fastapi import HTTPException
from app.schemas.role import RoleRequest, RoleResponse, RoleUpdate
from app.services.ids import id_generate
from sqlalchemy.orm import Session

from app.db.models import Role as RoleModel


class RoleUseCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def add_role(self, role: RoleRequest) -> dict[str, str]:
        try:
            role_on_db = self.db_session.query(RoleModel).filter_by(name=role.name).first()

            if role_on_db:
                raise HTTPException(status_code=400, detail="Cargo já cadastrado")

            role_on_db = RoleModel(**role.dict(), id=id_generate())

            self.db_session.add(role_on_db)
            self.db_session.commit()

            return {"msg": "Cargo cadastrado com sucesso"}

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def get_role(self, role_id: str) -> RoleResponse:
        try:
            role_db = self._role_model(role_id)

            role_response = RoleResponse(**role_db.dict())

            return role_response

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def get_all_roles(self) -> list[RoleResponse]:
        try:
            role_list = self.db_session.query(RoleModel).all()

            if not role_list:
                raise HTTPException(status_code=404, detail='Não há nenhum cargo cadastrado')

            return self._map_models_to_responses(role_list)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def update_role(self, role: RoleUpdate)  -> dict[str, str]:
        try:
            role_db = self._role_model(role.id)

            for field, value in role.dict().items():

                if value is not None:
                    setattr(role_db, field, value)
                else:
                    setattr(role_db, field, value)

            self.db_session.commit()
            self.db_session.refresh(role_db)

            return {"msg": "Cargo atualizado com sucesso"}

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def delete_role(self, role_id: str):
        try:
            role_db = self._role_model(role_id)

            self.db_session.delete(role_db)
            self.db_session.commit()

            return {"msg": "Cargo deletado com sucesso"}

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def _map_models_to_responses(self, roles: list[RoleModel]) -> list[RoleResponse]:
        return [RoleResponse(**role.dict()) for role in roles]

    def _role_model(self, role_id: str) -> RoleModel:

        role_db = (
            self.db_session
            .query(RoleModel)
            .filter_by(id=role_id)
            .first()
        )

        if not role_db:

            raise HTTPException(status_code=404, detail='Cargo não encontrado')

        return role_db

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Tecnologia as Model
from app.schemas.tecnologia import Request, Update, Response
from app.services.ids import id_generate

NAME_ENTITY = "Tecnologia"

class TecCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    
    def add(self, entity: Request) -> dict[str, str]:
        try:
            on_db = self.db_session.query(Model).filter_by(title=entity.title).first()
            
            if on_db:
                raise HTTPException(status_code=400, detail=f"{NAME_ENTITY} já cadastrado")

            on_db = Model(**entity.dict(), id=id_generate())
            self.db_session.add(on_db)

            self.db_session.commit()
            
            return {"msg": f"{NAME_ENTITY} cadastrado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def get(self, entity_id: str) -> Response:
        try:
            entity_db = self._entity_model_id(entity_id)
            entity_response = Response(**entity_db.dict())
            return entity_response
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def get_all(self) -> list[Response]:
        try:
            entity_list = self.db_session.query(Model).all()
            
            if not entity_list:
                raise HTTPException(status_code=404, detail=f"Não há nenhum {NAME_ENTITY} cadastrado")
            
            return self._map_models_to_responses(entity_list)
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def update(self, entity: Update) -> dict[str, str]:
        try:
            entity_db = self._entity_model_id(entity.id)
            
            for field, value in entity.dict().items():
                if value:
                    setattr(entity_db, field, value)
            
            self.db_session.commit()
            
            return {"msg": f"{NAME_ENTITY} atualizado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def delete(self, entity_id: str) -> dict[str, str]:
        try:
            entity_db = self._entity_model_id(entity_id)
            
            self.db_session.delete(entity_db)
            self.db_session.commit()
            
            return {"msg": f"{NAME_ENTITY} deletado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def _entity_model(self, entity_title: str) -> Model:
        entity_db = self.db_session.query(Model).filter_by(title=entity_title).first()
        
        if not entity_db:
            raise HTTPException(status_code=404, detail=f"{NAME_ENTITY} não encontrado")
        
        return entity_db
    
    def _entity_model_id(self, entity_id: str) -> Model:
        entity_db = self.db_session.query(Model).filter(Model.id == entity_id).first()
        
        if not entity_db:
            raise HTTPException(status_code=404, detail=f"{NAME_ENTITY} não encontrado")
        
        return entity_db

    def _map_models_to_responses(self, entitys: list[Model]) -> list[Response]:
        return [Response(**entity.dict()) for entity in entitys]
 
    # def _assemble_entity_response(self, entity: Model) -> Response:
    #     return Response(**entity.dict() for  in )

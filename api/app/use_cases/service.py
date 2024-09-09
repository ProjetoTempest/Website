from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.models import Service as ServiceModel
from app.db.models import ImagesService as ImageServiceModel
from app.schemas.service import ServiceRequest, ServiceUpdate, ServiceResponse
from app.schemas.images_services import ImagesServicesResponse
from app.services.ids import id_generate

class ServiceCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    
    def add(self, service: ServiceRequest) -> dict[str, str]:
        try:
            service_on_db = self.db_session.query(ServiceModel).filter_by(title=service.title).first()
            
            if service_on_db:
                raise HTTPException(status_code=400, detail="Serviço já cadastrado")

            service_on_db = ServiceModel(**service.model_dump(exclude={"images"}), id=id_generate())
            self.db_session.add(service_on_db)

            if not service.images:
                self.db_session.commit()
                return {"msg": "Serviço cadastrado com sucesso"}
            
            list_imgs = [ImageServiceModel(url=img_url, item_id=id, id=id_generate()) for img_url in service.images]

            self.db_session.add_all(list_imgs)

            service_on_db.images = list_imgs

            self.db_session.commit()
            
            return {"msg": "Serviço cadastrado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def get(self, service_id: str) -> ServiceResponse:
        try:
            service_db = self._service_model_id(service_id)
            service_response = self._assemble_service_response(service=service_db) 
            return service_response
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def get_all(self) -> list[ServiceResponse]:
        try:
            service_list = self.db_session.query(ServiceModel).options(joinedload(ServiceModel.images)).all()
            
            if not service_list:
                raise HTTPException(status_code=404, detail="Não há nenhum Serviço cadastrado")
            
            return self._map_models_to_responses(service_list)
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    # Fazer a atualização de imagens
    def update(self, service: ServiceUpdate) -> dict[str, str]:
        try:
            service_db = self._service_model_id(service.id)
            
            for field, value in service.dict().items():
                if value:
                    setattr(service_db, field, value)
            
            self.db_session.commit()
            
            return {"msg": "Serviço atualizado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def delete(self, service_id: str) -> dict[str, str]:
        try:
            service_db = self._service_model_id(service_id)
            
            self.db_session.delete(service_db)
            self.db_session.commit()
            
            return {"msg": "Serviço deletado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def _service_model(self, service_title: str) -> ServiceModel:
        service_db = self.db_session.query(ServiceModel).filter_by(title=service_title).first()
        
        if not service_db:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")
        
        return service_db
    
    def _service_model_id(self, service_id: str) -> ServiceModel:
        service_db = self.db_session.query(ServiceModel).filter(ServiceModel.id == service_id).options(joinedload(ServiceModel.images)).first()
        
        if not service_db:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")
        
        return service_db

    def _map_models_to_responses(self, services: list[ServiceModel]) -> list[ServiceResponse]:
        return [self._assemble_service_response(service=service) for service in services]
 
    def _assemble_service_response(self, service: ServiceModel) -> ServiceResponse:
        if not service.images:
            return ServiceResponse(**service.dict())
        return ServiceResponse(**service.dict(), images=[ImagesServicesResponse(**img.dict()) for img in service.images])
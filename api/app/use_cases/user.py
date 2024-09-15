from fastapi import HTTPException
from app.schemas.user import UserRequest, UserUpdate, UserResponse, UserResponseLogin
from app.services.ids import id_generate
from sqlalchemy.orm import Session

from app.db.models import User as UserModel
from app.db.models import Role as RoleModel
from app.schemas.login import Request
from app.services.tokens import generate_token, encode_token
from app.schemas.token import TokenData

class UserCases:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
    
    def add(self, user: UserRequest) -> dict[str, str]:
        try:
            user_on_db = self.db_session.query(UserModel).filter_by(email=user.email).first()
            
            if user_on_db:
                raise HTTPException(status_code=400, detail="Usuário já cadastrado")
            
            user_on_db = UserModel(**user.dict(), id=id_generate())
            
            self.db_session.add(user_on_db)
            self.db_session.commit()
            
            return {"msg": "Usuário cadastrado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def get(self, user_id: str) -> UserResponse:
        try:
            user_db = self._user_model_id(user_id)
            
            user_response = UserResponse(**user_db.dict())
            
            return user_response
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def get_all(self) -> list[UserResponse]:
        try:
            user_list = self.db_session.query(UserModel).all()
            print(user_list)
            if not user_list:
                raise HTTPException(status_code=404, detail="Não há nenhum usuário cadastrado")
            
            return self._map_models_to_responses(user_list)
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def update(self, user) -> dict[str, str]:
        try:
            user_db = self._user_model_id(user.id)
            
            for field, value in user.dict().items():
                if value:
                    setattr(user_db, field, value)
            
            self.db_session.commit()
            
            return {"msg": "Usuário atualizado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def delete(self, user_id: str) -> dict[str, str]:
        try:
            user_db = self._user_model_id(user_id)
            
            self.db_session.delete(user_db)
            self.db_session.commit()
            
            return {"msg": "Usuário deletado com sucesso"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def _user_model(self, user_email: str) -> UserModel:
        user_db = self.db_session.query(UserModel).filter_by(email=user_email).first()
        
        if not user_db:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return user_db
    
    def _user_model_id(self, user_id: str) -> UserModel:
        user_db = self.db_session.query(UserModel).filter_by(id=user_id).first()
        
        if not user_db:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return user_db

    def _map_models_to_responses(self, users: list[UserModel]) -> list[UserResponse]:
        return [UserResponse(**user.dict()) for user in users]
    
    def login(self, dados: Request) -> tuple:
        user = self.db_session.query(UserModel).filter(UserModel.email == dados.email, UserModel.password == dados.password).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # user_token = TokenData(id=user.id, name=user.name, email=user.email, role_name=user.role.name)
        user_token = TokenData(role_name=user.role.name)

        return encode_token(generate_token(user_token))
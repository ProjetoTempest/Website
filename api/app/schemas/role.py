from pydantic import model_validator, field_validator
from fastapi import HTTPException

from schemas.base import CustomBaseModel

class RoleRequest(CustomBaseModel):
    """
    - Attributes:
        - name: str
        - description: str | None
    """
    name: str | None = None
    description: str | None = None
    
    """
    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        
        if not password or not confirm_password:
            raise ValueError('Informe as duas senha corretamente')
        
        if password != confirm_password:
            raise ValueError('As senhas não coincidem')
        
        return values
    """
    
    
    @field_validator('name', mode='before')
    def validate_birth_date(cls, name):
        
        if name is None:
            raise HTTPException(status_code=400, detail='O campo nome é obrigatório')
        
        if not isinstance(name, str):
            raise HTTPException(status_code=400, detail='O campo nome precisa ser do tipo string')
        
        return name
    
    
"""class RoleInDB(RoleRequest):

    id: str
    class Config:
        from_attributes = True"""
        
class RoleUpdate(RoleRequest):
    """
    - Attributes:
        - id: str
        - name: str
        - description: str | None
    """
    id:str
    
    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        name = values.get('name')
        description = values.get('description')
        
        if not name and not description:
            raise HTTPException(400, "Informe ao menos um campo para atualizar")
        
        return values

        
class RoleResponse(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - name: str
        - description: str | None
    """
    id: str
    name: str
    description: str
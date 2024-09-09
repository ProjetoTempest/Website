from fastapi import HTTPException
from pydantic import field_validator, model_validator


from app.schemas.base import CustomBaseModel
from app.services.check_erros import Check_Error

class UserRequest(CustomBaseModel):
    """
    - Attributes:
        - name: str
        - email: str
        - password: str
        - role_id: str
        - photo: str
        - description: str
    """
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role_id: str | None = None
    photo: str | None = None
    description: str | None = None

    @model_validator(mode='before')
    def check_fields(cls, values):
        Check_Error.validate_required_string_field(values.get('name'), 'name')
        Check_Error.validate_required_string_field(values.get('email'), 'email')
        Check_Error.validate_required_string_field(values.get('password'), 'password')
        Check_Error.validate_required_string_field(values.get('role_id'), 'role_id')

        return values
    
class UserUpdate(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - name: str
        - email: str
        - password: str
        - role_id: str
        - photo: str
        - description: str
    """
    id: str
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role_id: str | None = None
    photo: str | None = None
    description: str | None = None

    @model_validator(mode='before')
    def check_fields_not_empty(cls, values):
        
        Check_Error.update_fields_empty(
            values.get('name'),
            values.get('email'),
            values.get('password'),
            values.get('role_id'),
            values.get('photo'),
            values.get('description')
        )

        return values
        


class UserResponse(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - name: str
        - email: str
        - role_id: str
        - photo: str
        - description: str
    """
    id: str | None = None
    name: str | None = None
    email: str | None = None
    role_id: str | None = None
    photo: str | None = None
    description: str | None = None
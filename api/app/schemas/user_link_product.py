from pydantic import model_validator
from app.schemas.base import CustomBaseModel

class Request(CustomBaseModel):
    """
    - Attributes:
        - title: str
        - description: str
        - link: str
        - icon: str
    """
    user_id: str | None = None
    products_id: str | None = None

    @model_validator(mode='before')
    def check_fields(cls, values):
        super().validate_required_string_field(field=values.get('user_id'), name_field='user_id')
        super().validate_required_string_field(field=values.get('products_id'), name_field='products_id')

        return values
    
class Update(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - title: str
        - description: str
        - link: str
        - icon: str
    """
    id: str
    user_id: str | None = None
    products_id: str | None = None

    @model_validator(mode='before')
    def check_fields_not_empty(cls, values):
        super().update_fields_empty(
            values.get('user_id'),
            values.get('products_id'),
        )

        return values
        
class Response(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - title: str
        - description: str
        - link: str
        - icon: str
    """
    id: str
    user_id: str | None = None
    products_id: str | None = None



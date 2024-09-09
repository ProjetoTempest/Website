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
    title: str | None = None
    description: str | None = None
    link: str | None = None
    icon: str | None = None

    @model_validator(mode='before')
    def check_fields(cls, values):
        super().validate_required_string_field(field=values.get('title'), name_field='title')
        super().validate_required_string_field(field=values.get('description'), name_field='description')
        super().validate_required_string_field(field=values.get('link'), name_field='link')
        super().validate_required_string_field(field=values.get('icon'), name_field='icon')

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
    title: str | None = None
    description: str | None = None
    link: str | None = None
    icon: str | None = None

    @model_validator(mode='before')
    def check_fields_not_empty(cls, values):
        super().update_fields_empty(
            values.get('title'),
            values.get('description'),
            values.get('link'),
            values.get('icon')
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
    title: str | None = None
    description: str | None = None
    link: str | None = None
    icon: str | None = None



from pydantic import model_validator
from app.schemas.base import CustomBaseModel
from app.schemas.images_services import ImagesServicesResponse

class ServiceRequest(CustomBaseModel):
    """
    - Attributes:
        - title: str
        - description: str
        - value: float
        - images: list[str]
    """
    title: str | None = None
    description: str | None = None
    value: float | None = None
    images: list[str] | None = None

    @model_validator(mode='before')
    def check_fields(cls, values):
        super().validate_required_string_field(values.get('title'), 'title')
        
        print("Aquil")
        # super().assert_float_value(values.get('value'), update=False)

        return values
    
class ServiceUpdate(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - title: str
        - description: str
        - value: float
        - images: list[str]
    """
    id: str
    title: str | None = None
    description: str | None = None
    value: float | None = None
    images: list[str] | None = None

    @model_validator(mode='before')
    def check_fields_not_empty(cls, values):
        super().update_fields_empty(
            values.get('title'),
            values.get('description'),
            values.get('value'),
            values.get('images')
        )
        super().assert_float_value(values.get('value'))

        return values
        
class ServiceResponse(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - title: str
        - description: str
        - value: float
        - images: list[ImagesServicesResponse]
    """
    id: str | None = None
    title: str | None = None
    description: str | None = None
    value: float | None = None
    images: list[ImagesServicesResponse] | None = None



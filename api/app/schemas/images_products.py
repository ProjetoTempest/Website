from pydantic import field_validator, model_validator
from app.schemas.base import CustomBaseModel

class ImagesProductsRequest(CustomBaseModel):
    """
    - Attributes:
        - url: str
        - item_id: str
    """
    url: str | None = None
    item_id: str | None = None

class ImagesProductsResponse(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - url: str
        - item_id: str
    """
    id: str
    url: str
    item_id: str

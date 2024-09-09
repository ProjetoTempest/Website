from app.schemas.base import CustomBaseModel

class ImagesServicesRequest(CustomBaseModel):
    """
    - Attributes:
        - url: str
        - item_id: str
    """
    url: str | None = None
    item_id: str | None = None

class ImagesServicesResponse(CustomBaseModel):
    """
    - Attributes:
        - id: str
        - url: str
        - item_id: str
    """
    id: str
    url: str
    item_id: str

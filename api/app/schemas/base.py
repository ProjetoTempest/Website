from pydantic import BaseModel
from fastapi import HTTPException


class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        """
        Converte a Classe em um dicionário
        """
        d = super().model_dump(*args, **kwargs)
        d = {k: v for k, v in d.items() if v is not None}
        return d

    @staticmethod
    def validate_required_string_field(field: str | None, name_field:str):
        if field is None or field == '':
            raise HTTPException(status_code=400, detail=f'O campo {name_field} é obrigatório')

        if not isinstance(field, str):
            raise HTTPException(status_code=400, detail=f'O campo {name_field} precisa ser do tipo string')
    
    @staticmethod
    def update_fields_empty(*args):
        if not any(args):
            raise HTTPException(400, "Informe ao menos um campo para atualizar")
        
    @staticmethod
    def assert_float_value(field: float | None, update: bool = True | False):
        if field is None and not update:
            raise HTTPException(400, "Informe um valor para o campo")
        if not isinstance(field, float) and not update:
            raise HTTPException(400, "O campo precisa ser do tipo float")
        if field is not None:
            if field <= 0:
                raise HTTPException(400, "O campo precisa ser maior que zero")
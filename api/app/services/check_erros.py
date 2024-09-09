from fastapi import HTTPException

class Check_Error:
    @staticmethod
    def validate_required_string_field(campo, name_campo:str):
        if campo is None or campo == '':
            raise HTTPException(status_code=400, detail=f'O campo {name_campo} é obrigatório')

        if not isinstance(campo, str):
            raise HTTPException(status_code=400, detail=f'O campo {name_campo} precisa ser do tipo string')
    
    @staticmethod
    def update_fields_empty(*args):
        if not any(args):
            raise HTTPException(400, "Informe ao menos um campo para atualizar")
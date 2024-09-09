import pytest
from fastapi import HTTPException

from app.schemas.role import RoleRequest, RoleUpdate
from app.use_cases.role import RoleUseCases


def test_role_request():
    role_request = RoleRequest(name='role_test', description='role_test_description')
    assert role_request.name == 'role_test'
    assert role_request.description == 'role_test_description'


def test_invalid_role_request_empty_name_sem_nada():

    with pytest.raises(HTTPException) as excinfo:
        RoleRequest(name=None, description='')

    print(str(excinfo.value))

    assert "O campo nome é obrigatório" in str(excinfo.value)


def test_invalid_role_request_empty_name():
    # Testa a criação de RoleRequest com nome vazio
    with pytest.raises(HTTPException) as excinfo:
        RoleRequest(name="", description="Some description")

    # O detalhe do erro deve conter a mensagem esperada de `ValueError`
    assert "O campo nome é obrigatório" in str(excinfo.value)


def test_invalid_role_request_non_string_name():
    with pytest.raises(HTTPException) as excinfo:
        RoleRequest(name=123, description="Some description")

    assert "O campo nome precisa ser do tipo string" in str(excinfo.value)


def test_role_update():
    role_update = RoleUpdate(id='1', name='role_test', description='role_test_description')
    assert role_update.id == '1'
    assert role_update.name == 'role_test'
    assert role_update.description == 'role_test_description'


def test_invalid_role_update_empty_name():
    with pytest.raises(HTTPException) as excinfo:
        RoleUpdate(id='1', name='', description='role_test_description')

    assert "Informe ao menos um campo para atualizar" in str(excinfo.value)

def test_add_role(role_use_cases):
    role_request = RoleRequest(name="name_test", description="description_test")
    response = role_use_cases.add_role(role_request)
    assert response == {"msg": "Cargo cadastrado com sucesso"}

def test_add_role_already_exists(role_use_cases):
    role_request = RoleRequest(name="name_test", description="description_test")
    
    role_use_cases.add_role(role_request)
    
    with pytest.raises(HTTPException) as excinfo:
        role_use_cases.add_role(role_request)
    
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Cargo já cadastrado"

def test_get_role(role_use_cases):
    role_request = RoleRequest(name="name_test", description="description_test")
    role_use_cases.add_role(role_request)

    id = role_use_cases.get_all_roles()[0].id
    
    role = role_use_cases.get_role(role_id=id)
    
    assert role.name == "name_test"
    assert role.description == "description_test"

def test_get_role_not_found(role_use_cases):
    with pytest.raises(HTTPException) as excinfo:
        role_use_cases.get_role(role_id='1')
    
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Cargo não encontrado"

def test_get_all_role(role_use_cases):
    role_request = RoleRequest(name="name_test", description="description_test")
    role_use_cases.add_role(role_request)

    role_request = RoleRequest(name="name_test1", description="description_test1")

    role_use_cases.add_role(role_request)

    list_roles = role_use_cases.get_all_roles()

    assert len(list_roles) == 2

def test_get_all_role_not_found(role_use_cases):
    with pytest.raises(HTTPException) as excinfo:
        role_use_cases.get_all_roles()

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Não há nenhum cargo cadastrado"

def test_update_role(role_use_cases):

    role_request = RoleRequest(name="name_test", description="description_test")

    role_use_cases.add_role(role_request)

    id = role_use_cases.get_all_roles()[0].id

    role_update = RoleUpdate(id=id, name='updated_role', description='updated_description')
    response = role_use_cases.update_role(role_update)
    assert response == {"msg": "Cargo atualizado com sucesso"}

def test_update_role_not_found(role_use_cases):
    with pytest.raises(HTTPException) as excinfo:
        role_update = RoleUpdate(id='non_existing_id', name='updated_role', description='updated_description')
        role_use_cases.update_role(role_update)
    
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Cargo não encontrado"

def test_delete_role(role_use_cases):
        role_request = RoleRequest(name="name_test", description="description_test")
        role_use_cases.add_role(role_request)

        id = role_use_cases.get_all_roles()[0].id

        response = role_use_cases.delete_role(role_id=id)
        assert response == {"msg": "Cargo deletado com sucesso"}

        with pytest.raises(HTTPException) as excinfo:
            role_use_cases.get_role(role_id=id)

        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == "Cargo não encontrado"

def test_delete_role_not_found(role_use_cases):
    with pytest.raises(HTTPException) as excinfo:
        role_use_cases.delete_role(role_id='non_existing_id')
    
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Cargo não encontrado"
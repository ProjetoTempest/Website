import pytest
from fastapi import HTTPException, status

from app.schemas.role import RoleRequest, RoleUpdate
from app.use_cases.role import RoleUseCases

def test_create_user(client):
    response = client.post(
        '/users',
        json={
            "name": "string",
            "email": "string",
            "password": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"msg": "Usuário cadastrado com sucesso"}

def test_create_user_already_exists(client):
    response = client.post(
        '/users',
        json={
            "name": "string",
            "email": "string",
            "password": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
},
    )

    response = client.post(
        '/users',
        json={
            "name": "string",
            "email": "string",
            "password": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Usuário já cadastrado"}

def test_create_user_empty_name(client):
    response = client.post(
        '/users',
        json={
            "name": "",
            "email": "string",
            "password": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'O campo name é obrigatório',
    }

def test_create_user_empty_email(client):
    response = client.post(
        '/users',
        json={
            "name": "string",
            "email": "",
            "password": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'O campo email é obrigatório',
    }


def test_create_user_empty_password(client):
    response = client.post(
        '/users',
        json={
            "name": "string",
            "email": "string",
            "password": "",
            "role_id": "string",
            "photo": "string",
            "description": "string"
},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'O campo password é obrigatório',
    }

def test_create_user_empty_role_id(client):
    response = client.post(
        '/users',
        json={
            "name": "string",
            "email": "string",
            "password": "string",
            "role_id": "",
            "photo": "string",
            "description": "string"
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'O campo role_id é obrigatório',
    }

# def test_create_user_empty_photo(client):
#     response = client.post(
#         '/users',
#         json={
#             "name": "string",
#             "email": "string",
#             "password": "string",
#             "role_id": "string",
#             "photo": "",
#             "description": "string"
# },
#     )

#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert response.json() == {
#         'detail': 'O campo photo é obrigatório',
#     }

# def test_get_user(client):
#     response = client.get('/users/1')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {
#         "name": "string",
#         "email": "string",
#         "role_id": "string",
#         "photo": "string",
#         "description": "string"
    # }

def test_get_all_users(client):
    response = client.post(
        '/users',
        json={
            "name": "string",
            "email": "string",
            "password": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
        },
    )


    response = client.get('/users/all/') 

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": response.json()[0]["id"],
            "name": "string",
            "email": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
        },
    ]

def test_get_all_users_empty(client):
    response = client.get('/users/all/') 

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Não há nenhum usuário cadastrado'
        }

def test_update_user(client):
    client.post(
        '/users',
        json={
            "name": "string",
            "email": "string",
            "password": "string",
            "role_id": "string",
            "photo": "string",
            "description": "string"
        },
    )

    response = client.get('/users/all/') 

    id = response.json()[0]["id"]
        
    response = client.put(
        '/users/update/',
        json={
        "id": f"{id}",
        "name": "string",
        "email": "string",
        "password": "string",
        "role_id": "string",
        "photo": "string",
        "description": "string"
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "msg": "Usuário atualizado com sucesso"
        }
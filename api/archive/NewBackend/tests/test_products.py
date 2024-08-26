# tests/test_products.py
import pytest
from fastapi import status

# Teste da criação de produto
def test_create_product(client):
    product_data = {
        "title": "Produto Teste",
        "description": "Descrição do Produto Teste",
        "value": 99.99,
        "images": []
    }

    response = client.post("/products/", json=product_data)
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == product_data["title"]
    assert response.json()["description"] == product_data["description"]
    assert response.json()["value"] == product_data["value"]

# Teste de leitura de produtos
def test_read_products(client):
    response = client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

# Teste de leitura de produto por ID
def test_read_product(client):
    # Primeiro cria um produto para testar a leitura por ID
    product_data = {
        "title": "Produto Teste",
        "description": "Descrição do Produto Teste",
        "value": 99.99,
        "images": []
    }
    response = client.post("/products/", json=product_data)
    product_id = response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == product_data["title"]

# Teste de atualização de produto
def test_update_product(client):
    # Cria um produto para testar a atualização
    product_data = {
        "title": "Produto Original",
        "description": "Descrição Original",
        "value": 59.99,
        "images": []
    }
    response = client.post("/products/", json=product_data)
    product_id = response.json()["id"]

    updated_product_data = {
        "title": "Produto Atualizado",
        "description": "Descrição Atualizada",
        "value": 79.99
    }
    response = client.put(f"/products/update/{product_id}", json=updated_product_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == updated_product_data["title"]
    assert response.json()["description"] == updated_product_data["description"]
    assert response.json()["value"] == updated_product_data["value"]

# Teste de exclusão de produto
def test_delete_product(client):
    # Cria um produto para testar a exclusão
    product_data = {
        "title": "Produto a ser Deletado",
        "description": "Descrição",
        "value": 49.99,
        "images": []
    }
    response = client.post("/products/", json=product_data)
    product_id = response.json()["id"]

    response = client.delete(f"/products/delete/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Product deleted successfully"

    # Verifica se o produto foi realmente excluído
    response = client.get(f"/products/{product_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found"

# Teste de criação de produto com dados inválidos
def test_create_product_invalid_data(client):
    product_data = {
        "title": "",
        "description": "Descrição",
        "value": -10.00,
        "images": []
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

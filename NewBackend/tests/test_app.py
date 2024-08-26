from fastapi.testclient import TestClient  
from http import HTTPStatus 
from  newbackend.main import app  

client = TestClient(app)

def test_root_deve_retornar_ok_e_ola_mundo():  
    client = TestClient(app)  

    response = client.get('/users')  

    assert response.status_code == HTTPStatus.OK  
    assert response.json() == [] 
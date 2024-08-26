from pytest import raises

from schemas.role import (
    RoleRequest,
    RoleUpdate,
    RoleResponse
    )

def test_role_request():
    role_request = RoleRequest(name='role_test', description='role_test_description')
    assert role_request.name == 'role_test'
    assert role_request.description == 'role_test_description'
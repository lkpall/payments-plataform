import pytest


@pytest.mark.anyio
async def test_get_user_by_id_should_return_success(client, create_user_fixture):
    response = await client.get(f"/users/{create_user_fixture.id}")
    expected_response = {
        'id': create_user_fixture.id,
        'name': create_user_fixture.name,
        'email': create_user_fixture.email,
        'role': create_user_fixture.role,
        'status': create_user_fixture.status
    }
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.anyio
async def test_get_user_by_id_should_return_not_found(client):
    response = await client.get("/users/1")
    expected_response = {'detail': 'User not found'}
    assert response.status_code == 404
    assert response.json() == expected_response

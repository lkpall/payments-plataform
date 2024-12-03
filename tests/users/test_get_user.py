import pytest

from tests.conftest import MOCK_SESSION


@pytest.mark.anyio
async def test_get_user_should_return_success(client, create_user_fixture):
    response = await client.get("/users/")
    expected_response = {
        'id': create_user_fixture.id,
        'name': create_user_fixture.name,
        'email': create_user_fixture.email,
        'role': create_user_fixture.role,
        'status': create_user_fixture.status
    }
    assert response.status_code == 200
    assert response.json()[0] == expected_response


@pytest.mark.anyio
async def test_get_user_should_return_empty_list(client):
    response = await client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

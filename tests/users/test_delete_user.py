import pytest


@pytest.mark.anyio
async def test_delete_user_should_return_success(client, create_user_fixture):
    response = await client.delete(f"/users/{create_user_fixture.id}")
    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_user_should_return_user_not_found(client):
    response = await client.delete("/users/1")
    expected_response = {'detail': 'User not found'}
    assert response.status_code == 404
    assert response.json() == expected_response

import pytest

@pytest.mark.anyio
async def test_create_user(client):
    response = await client.get("/api/healtcheck")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is On!"}

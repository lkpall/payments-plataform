import pytest

@pytest.mark.anyio
async def test_create_user(client):
    body = {
        'name': 'Matheus',
        'email': 'mfp186@hotmail.com',
        'role': 1,
        'registro_nacional': '01669581403',
        'password': 'batatinha'
    }
    response = await client.post("/users/", json=body)
    expected_response = {
        'id': 1,
        'name': 'Matheus',
        'email': 'mfp186@hotmail.com',
        'role': 1,
        'status': True
    }
    assert response.status_code == 200
    assert response.json() == expected_response
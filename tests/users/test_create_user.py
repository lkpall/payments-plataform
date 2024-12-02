import pytest

from sqlalchemy.exc import IntegrityError

from tests.conftest import MOCK_SESSION


BODY = {
    'name': 'Matheus',
    'email': 'mfpo159@hotmail.com',
    'role': 1,
    'registro_nacional': '01869781104',
    'password': 'batatinha'
}

@pytest.mark.anyio
async def test_create_user_should_return_success(client):
    response = await client.post("/users/", json=BODY)
    expected_response = {
        'id': 1,
        'name': 'Matheus',
        'email': 'mfpo159@hotmail.com',
        'role': 1,
        'status': True
    }
    assert response.status_code == 201
    assert response.json() == expected_response


@pytest.mark.anyio
async def test_create_user_should_return_internal_error(client, mocker):
    expected_response = {'detail': 'An unexpected error occurred.'}
    mock_create_wallet = mocker.patch('app.views.users.create_wallet')
    mock_create_wallet.side_effect = Exception('Teste')
    response = await client.post("/users/", json=BODY)
    assert response.status_code == 500
    assert response.json() == expected_response


@pytest.mark.anyio
async def test_create_user_should_return_integrity_error(mock_client, mocker):
    body = BODY.copy()
    body.update({'id': 1})
    MOCK_SESSION.commit.side_effect = IntegrityError('teste', {'test': 't'}, Exception('Error'))

    response = await mock_client.post("/users/", json=body)
    expected_response = {'detail': 'User already exists or violates database constraints.'}

    assert response.status_code == 409
    assert response.json() == expected_response

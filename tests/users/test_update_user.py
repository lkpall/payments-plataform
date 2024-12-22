import pytest

BODY = {
    'name': 'Matheus',
    'email': 'mfpo159@hotmail.com',
    'role': 1,
    'identity_number': '01869781104',
    'password': 'batatinha'
}


@pytest.mark.anyio
async def test_update_user_should_return_success(client, create_user_fixture, mocker):
    mock_encrypt_password = mocker.patch('app.views.users.encrypt_password')
    mock_encrypt_password.return_value = 'testado'

    response = await client.patch(f"/users/{create_user_fixture.id}", json=BODY)
    expected_response = {
        'id': create_user_fixture.id,
        'name': BODY['name'],
        'email': BODY['email'],
        'role': BODY['role'],
        'status': True
    }

    mock_encrypt_password.assert_called_once_with(BODY['password'])
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.anyio
async def test_update_user_should_return_user_not_found(client):
    response = await client.patch("/users/1", json=BODY)
    expected_response = {'detail': 'User not found'}
    assert response.status_code == 404
    assert response.json() == expected_response

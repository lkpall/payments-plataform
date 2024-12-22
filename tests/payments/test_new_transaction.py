import pytest

from unittest.mock import AsyncMock

from tests.payments import MOCK_WALLET_USER_1, MOCK_WALLET_USER_2


BODY = {
    'payer': 1,
    'payee': 2,
    'amount': 29
}


@pytest.mark.anyio
async def test_create_new_transaction_should_return_ok_and_uuid(
    client, create_users_fixture, mocker
):
    # mock wallet users
    mocked_user1 = AsyncMock()
    mocked_user1.wallet.id = MOCK_WALLET_USER_1['id']
    mocked_user2 = AsyncMock()
    mocked_user2.wallet.id = MOCK_WALLET_USER_2['id']

    # mock functions
    mock_get_user = mocker.patch('app.views.payments.get_user')
    mock_get_user.side_effect = [mocked_user1, mocked_user2]

    mock_check_payer_balance_is_valid = mocker.patch(
        'app.views.payments.check_payer_balance_is_valid'
    )
    mock_authorize_transaction = mocker.patch(
        'app.views.payments.authorize_transaction'
    )

    # request
    response = await client.post('/transfer/', json=BODY)

    # asserts
    mock_check_payer_balance_is_valid.assert_called_once_with(
        mocked_user1, BODY['amount']
    )
    mock_authorize_transaction.assert_awaited_once()
    mock_authorize_transaction.assert_called_once()
    assert response.status_code == 201
    assert response.json()['ok']
    assert response.json().get('transaction_id')

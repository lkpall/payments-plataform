from decimal import Decimal

import pytest

from fastapi import HTTPException

from app.utils.payments import (
    authorize_transaction,
    check_payer_balance_is_valid,
    get_user
)

from unittest.mock import AsyncMock

from tests.payments import MOCK_USER_2


class HttpxStub:
    def __init__(self, authorization: bool = True):
        self.authorization = authorization

    def json(self):
        return {"data": {"authorization": self.authorization}}


@pytest.mark.anyio
async def test_get_user_should_return_user(db_session, create_users_fixture):
    user = await get_user(db_session, MOCK_USER_2['id'])
    res = user.model_dump()

    for k, v in MOCK_USER_2.items():
        assert res[k] == v


@pytest.mark.anyio
async def test_get_user_should_return_user_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        await get_user(db_session, MOCK_USER_2['id'])

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.anyio
async def test_check_payer_balance_is_valid_should_work_without_give_error():
    user = AsyncMock()
    user.wallet.balance = Decimal('48.123')
    result = await check_payer_balance_is_valid(
        user,
        Decimal('11.156')
    )
    assert result is None


@pytest.mark.anyio
async def test_check_payer_balance_is_valid_should_return_insufficient_value():
    user = AsyncMock()
    user.wallet.balance = Decimal('11.156')

    with pytest.raises(HTTPException) as exc_info:
        await check_payer_balance_is_valid(
            user,
            Decimal('48.123')
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Insufficient value"


@pytest.mark.anyio
async def test_authorize_transaction_must_commit_complete_transaction(mocker):
    mocked_payer_wallet = mocker.AsyncMock(balance=Decimal('10'))
    mocked_payee_wallet = mocker.AsyncMock(balance=Decimal('20'))
    mocked_transaction = mocker.AsyncMock(amount=Decimal('5'), status='PENDING')
    mocked_session = mocker.AsyncMock()
    mocked_httpx = mocker.patch("app.utils.payments.httpx.AsyncClient")
    mocked_httpx().__aenter__.return_value.get.return_value = HttpxStub()

    await authorize_transaction(
        mocked_session,
        mocked_transaction,
        mocked_payer_wallet,
        mocked_payee_wallet
    )

    assert mocked_payer_wallet.balance == Decimal('5')
    assert mocked_payee_wallet.balance == Decimal('25')
    assert mocked_transaction.status == 'COMPLETED'
    mocked_session.commit.assert_called_once()


@pytest.mark.anyio
async def test_authorize_transaction_must_commit_failed_transaction(mocker):
    mocked_payer_wallet = mocker.AsyncMock(balance=Decimal('10'))
    mocked_payee_wallet = mocker.AsyncMock(balance=Decimal('20'))
    mocked_transaction = mocker.AsyncMock(amount=Decimal('5'), status='PENDING')
    mocked_session = mocker.AsyncMock()
    mocked_httpx = mocker.patch("app.utils.payments.httpx.AsyncClient")
    mocked_httpx().__aenter__.return_value.get.return_value = HttpxStub(
        authorization=False
    )

    with pytest.raises(HTTPException) as exc_info:
        await authorize_transaction(
            mocked_session,
            mocked_transaction,
            mocked_payer_wallet,
            mocked_payee_wallet
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Unauthorized transaction"
    assert mocked_transaction.status == 'FAILED'
    mocked_session.commit.assert_called_once()

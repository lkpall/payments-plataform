import pytest

from app.models.users import User
from app.models.wallet import Wallet

from tests.payments import (
    MOCK_USER_1, MOCK_USER_2, MOCK_WALLET_USER_1, MOCK_WALLET_USER_2
)


@pytest.fixture(scope="function")
async def create_users_fixture(db_session):
    user = User(**MOCK_USER_1)
    db_session.add(user)

    user2 = User(**MOCK_USER_2)
    db_session.add(user2)

    await db_session.flush()
    await db_session.refresh(user)
    await db_session.refresh(user2)

    user_wallet = Wallet(**MOCK_WALLET_USER_1)
    user2_wallet = Wallet(**MOCK_WALLET_USER_2)

    db_session.add(user_wallet)
    db_session.add(user2_wallet)

    await db_session.commit()

    yield [user, user2]

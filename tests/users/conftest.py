import pytest

from app.models.users import User


@pytest.fixture(scope="function")
async def create_user_fixture(db_session):
    user = User(
        name='Bruno',
        email='bruno@gmail.com',
        identity_number='01895142681',
        password='batatinha'
    )
    db_session.add(user)

    await db_session.commit()
    await db_session.refresh(user)

    yield user

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.infrastructure.db import get_session
from app.instance.config import settings
from main import app

from sqlalchemy import text

from app.models.users import UserType


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

async_engine = create_async_engine(
    settings.DB_URL,
    echo=True,
    future=True
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=async_engine,
    class_=AsyncSession
)

async def truncate_tables():
    async with async_engine.connect() as conn:
        await conn.execute(text("ALTER SEQUENCE _user_id_seq RESTART WITH 1;"))
        await conn.execute(text("DELETE FROM user_type;"))
        await conn.commit()

async def setup_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with TestingSessionLocal() as session:
        user_type = UserType(
            id=1,
            title='Admin'
        )
        session.add(user_type)
        await session.commit()

@pytest.fixture(scope="session", autouse=True)
async def setup():
    await truncate_tables()
    print("Iniciando os testes...")
    await setup_database()
    yield

@pytest.fixture(scope="function")
async def db_session():
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            async with TestingSessionLocal(bind=connection) as session:
                yield session
                await session.rollback()
                await transaction.rollback()

@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app), base_url=settings.BASE_URL) as test_client:
        yield test_client
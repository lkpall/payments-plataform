from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.instance.config import settings


async_engine = create_async_engine(
    url=settings.DB_URL,
    echo=True,
    future=True
)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

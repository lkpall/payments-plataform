from typing import Annotated

from fastapi import HTTPException, Query, APIRouter, status

from sqlalchemy.exc import IntegrityError

from sqlmodel import select

from app.common.encrypt_passwd import encrypt_password
from app.infrastructure.db import SessionDep
from app.models.users import User, UserResponse
from app.views.wallet.wallet import create_wallet


app = APIRouter(prefix="/users")


@app.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: User, session: SessionDep):
    try:
        user.password = encrypt_password(user.password)

        session.add(user)
        await session.flush()
        await session.refresh(user)

        new_wallet = create_wallet(user.id)
        session.add(new_wallet)
        await session.commit()
        return user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists or violates database constraints.",
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


@app.get("/", response_model=list[UserResponse])
async def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = await session.exec(select(User).offset(offset).limit(limit))
    return users


@app.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, session: SessionDep):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, user: User, session: SessionDep):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = encrypt_password(user.password)
    new_user_data = user.model_dump(exclude_unset=True)

    db_user.sqlmodel_update(new_user_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return user


@app.delete("/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"ok": True}

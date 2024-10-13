from typing import Annotated

from fastapi import HTTPException, Query, APIRouter
from sqlmodel import select

from app.common.encrypt_passwd import encrypt_password
from .models import User, UserResponse
from app.db.db import SessionDep


app = APIRouter(prefix="/users")


@app.post("/", response_model=UserResponse)
def create_user(user: User, session: SessionDep):
    user.password = encrypt_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/", response_model=list[UserResponse])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, user: User, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = encrypt_password(user.password)
    new_user_data = user.model_dump(exclude_unset=True)

    db_user.sqlmodel_update(new_user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return user


@app.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

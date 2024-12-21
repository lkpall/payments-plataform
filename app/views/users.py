from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.common.encrypt_passwd import encrypt_password
from app.infrastructure.db import SessionDep
from app.models.users import User, UserResponse
from app.views.wallet.wallet import create_wallet


app = APIRouter(prefix="/users")


@app.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: User, session: SessionDep):
    """User creation route

    Args:
        user (User): SQLModel object representing the user to be created
        session (SessionDep): Async session db

    Returns:
        status_code: Response status code
        user (UserResponse): Information of the user who was created

    Raises:
        HTTPException: If an integrity or insertion error occurs in the database
    """
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


@app.get("/", response_model=List[UserResponse])
async def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[UserResponse]:
    """Route to search for created users

    Args:
        session (SessionDep): Async session db
        offset (int): Offset value
        limit (int): Limit of users to bring per page

    Returns:
        status_code: Response status code
        List[UserResponse]: User list
    """
    users = await session.exec(select(User).offset(offset).limit(limit))
    return users


@app.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, session: SessionDep):
    """Search for specific user

    Args:
        user_id (int): ID User
        session (SessionDep): Async session db

    Returns:
        status_code: Response status code
        user (UserResponse): Information of the user who was created

    Raises:
        HTTPException: If user not found
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, user: User, session: SessionDep):
    """Update information for a specific user

    Args:
        user_id (int): User ID to be updated
        user (User): SQLModel object containing the user information to be updated
        session (SessionDep): Async session db

    Returns:
        status_code: Response status code
        user (UserResponse): Information of the user who was updated

    Raises:
        HTTPException: If user not found
    """
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.password:
        user.password = encrypt_password(user.password)

    new_user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(new_user_data)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@app.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep):
    """Delete specific user

    Args:
        user_id (int): ID User
        session (SessionDep): Async session db

    Returns:
        status_code: Response status code

    Raises:
        HTTPException: If user not found
    """
    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return {}

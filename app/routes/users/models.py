from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)


class User(UserBase, table=True):
    __tablename__ = "_user"
    registro_nacional: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)


class UserResponse(UserBase):
    id: int

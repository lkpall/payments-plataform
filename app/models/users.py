from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .wallet import Wallet


class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    role: int = Field(nullable=True, default=1, foreign_key="user_type.id")
    status: bool = Field(nullable=False, default=True)


class UserResponse(UserBase):
    id: int


class User(UserBase, table=True):
    __tablename__ = "_user"
    registro_nacional: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)

    wallet: Wallet = Relationship(back_populates="user")


class UserType(SQLModel, table=True):
    __tablename__ = "user_type"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)

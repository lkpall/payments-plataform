import uuid

from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship


class Wallet(SQLModel, table=True):
    __tablename__ = "wallet"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    balance: Decimal = Field(default=0, max_digits=5, decimal_places=3)
    user_id: int = Field(nullable=False, foreign_key="_user.id")

    transaction_history: list["Transaction"] = Relationship(back_populates="wallet")

class Transaction(SQLModel, table=True):
    __tablename__ = "transaction"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    type: str = Field(nullable=False)
    value: Decimal = Field(default=0, max_digits=5, decimal_places=3)

    wallet_id: uuid.UUID = Field(nullable=False, foreign_key="wallet.id")
    wallet: Wallet = Relationship(back_populates="transaction_history")

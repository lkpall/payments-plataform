import uuid

from decimal import Decimal

from typing import List

from sqlmodel import Field, SQLModel, Relationship



class Wallet(SQLModel, table=True):
    __tablename__ = "wallet"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    balance: Decimal = Field(default=0, max_digits=5, decimal_places=3)
    user_id: int = Field(nullable=False, foreign_key="_user.id")

    user: "User" = Relationship(back_populates="wallet")

    transaction_history_payer: List["Transaction"] = Relationship(
        back_populates="sender_wallet",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Transaction.sender_wallet_id == Wallet.id",
            "foreign_keys": "Transaction.sender_wallet_id"
        },
    )
    transaction_history_payee: List["Transaction"] = Relationship(
        back_populates="recipient_wallet",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Transaction.recipient_wallet_id == Wallet.id",
            "foreign_keys": "Transaction.recipient_wallet_id"
        },
    )

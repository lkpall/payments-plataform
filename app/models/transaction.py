import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel


class TransactionType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"


class TransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class Transaction(SQLModel, table=True):
    __tablename__ = "transaction"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )
    amount: Decimal = Field(nullable=False, max_digits=10, decimal_places=2)
    type: TransactionType = Field(
        sa_column=Column(
            Enum(TransactionType, name="transaction_type", native_enum=True),
            nullable=False
        ),
    )
    status: TransactionStatus = Field(
        sa_column=Column(
            Enum(TransactionStatus, name="transaction_status", native_enum=True),
            nullable=False
        ),
    )
    sender_wallet_id: uuid.UUID = Field(nullable=False, foreign_key="wallet.id")
    recipient_wallet_id: uuid.UUID = Field(nullable=False, foreign_key="wallet.id")
    timestamp: Optional[datetime] = Field(
        nullable=False, default_factory=datetime.utcnow
    )

    sender_wallet: Optional['Wallet'] = Relationship(  # NOQA
        back_populates="transaction_history_payer",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "Transaction.sender_wallet_id"
        },
    )
    recipient_wallet: Optional['Wallet'] = Relationship(  # NOQA
        back_populates="transaction_history_payee",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "Transaction.recipient_wallet_id"
        },
    )


class TransactionRequest(SQLModel):
    amount: Decimal = Field(nullable=False, max_digits=10, decimal_places=2)
    payer: int = Field(nullable=False)
    payee: int = Field(nullable=False)


class TransactionResponse(SQLModel):
    ok: bool
    transaction_id: uuid.UUID

from decimal import Decimal

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.infrastructure.db import SessionDep
from app.models.transaction import Transaction, TransactionStatus
from app.models.users import User
from app.models.wallet import Wallet


async def get_user(session: SessionDep, user_id: int) -> User:
    """Search the user

    Args:
        session (SessionDep): Async session db
        user_id (int): ID user

    Returns:
        User: user sqlalchemy instance

    Raises:
        HTTPException: If user_id not found
    """
    user = (
        await session.exec(
            select(User).options(joinedload(User.wallet)).where(User.id == user_id)
        )
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def check_payer_balance_is_valid(user: User, amount: Decimal):
    """Checks whether the payer's wallet has sufficient balance
        to carry out the transaction

    Args:
        user (User): user instance
        amount (Decimal): amount requested for transaction

    Raises:
        HTTPException: If insufficient value to carry out transaction
    """
    if user.wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient value")

    return


async def authorize_transaction(
        session: SessionDep,
        transaction: Transaction,
        payer_wallet: Wallet,
        payee_wallet: Wallet
):
    """Checks whether the external service allows the transaction to be carried out

    Raises:
        HTTPException: If not allowed raise unauthorized transaction
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://util.devi.tools/api/v2/authorize', timeout=5
            )
            is_authorized = response.json()['data']['authorization']

        if not is_authorized:
            transaction.status = TransactionStatus.FAILED
            await session.commit()

            raise HTTPException(status_code=400, detail="Unauthorized transaction")

        payer_wallet.balance -= transaction.amount
        payee_wallet.balance += transaction.amount

        transaction.status = TransactionStatus.COMPLETED
        await session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e

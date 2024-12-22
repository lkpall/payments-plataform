import logging

from fastapi import APIRouter

from app.infrastructure.db import SessionDep
from app.models.transaction import (
    Transaction,
    TransactionRequest,
    TransactionResponse,
    TransactionStatus,
    TransactionType
)
from app.utils.payments import (
    authorize_transaction,
    check_payer_balance_is_valid,
    get_user
)


router = APIRouter(prefix="/transfer")

logger = logging.getLogger("transactions_router")


@router.post('/', response_model=TransactionResponse, status_code=201)
async def transaction(transfer_data: TransactionRequest, session: SessionDep):
    """Performs banking transactions between payer and receiver accounts

    Args:
        tranfer_data (TransactionRequest): user's info
        session (SessionDep): Async session db

    Returns:
        The return value. True for success, False otherwise.

    Raises:
    """
    logger.info(f'Starting transaction for payer {transfer_data.payer}')

    payer = await get_user(session, transfer_data.payer)
    payee = await get_user(session, transfer_data.payee)

    await check_payer_balance_is_valid(payer, transfer_data.amount)

    new_transaction = Transaction(
        amount=transfer_data.amount,
        type=TransactionType.TRANSFER,
        status=TransactionStatus.PENDING,
        sender_wallet_id=payer.wallet.id,
        recipient_wallet_id=payee.wallet.id
    )

    session.add(new_transaction)
    await session.flush()
    await session.refresh(new_transaction)

    await authorize_transaction(
        session,
        new_transaction,
        payer.wallet,
        payee.wallet
    )

    return {'ok': True, "transaction_id": new_transaction.id}

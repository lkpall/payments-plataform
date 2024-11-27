from decimal import Decimal

from app.models.wallet import Wallet


def create_wallet(user_id: int, balance: Decimal = 0) -> Wallet:
    return Wallet(user_id=user_id, balance=balance)

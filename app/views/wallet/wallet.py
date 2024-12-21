from decimal import Decimal

from app.models.wallet import Wallet


def create_wallet(user_id: int, balance: Decimal = 0) -> Wallet:
    """Creates a new instance of the Wallet entity

    Args:
        user_id (int): ID user
        balance (balance): Wallet balance

    Returns:
        Wallet: Wallet object
    """
    return Wallet(user_id=user_id, balance=balance)

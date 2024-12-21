import hashlib


def encrypt_password(passwd: str) -> str:
    """Encrypts the received value

    Args:
        passwd (str): value

    Returns:
        str: Encrypted value
    """
    return hashlib.sha256(passwd.encode(encoding='utf-8')).hexdigest()

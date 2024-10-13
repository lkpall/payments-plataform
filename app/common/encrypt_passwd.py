import hashlib


def encrypt_password(passwd: str) -> str:
    return hashlib.sha256(passwd.encode(encoding='utf-8')).hexdigest()

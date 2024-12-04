import hashlib

from app.common.encrypt_passwd import encrypt_password


def test_encript_password():
    passwd = 'test_payments_plataform123@'
    result = encrypt_password(passwd)
    assert isinstance(result, str)
    assert hashlib.sha256(
        passwd.encode(encoding='utf-8')
    ).hexdigest() == result

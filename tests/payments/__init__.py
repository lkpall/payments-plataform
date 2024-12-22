from decimal import Decimal


MOCK_USER_1 = {
    'id': 3,
    'name': 'Bruno',
    'email': 'bruno@gmail.com',
    'identity_number': '01895142681',
    'password': 'batatinha'
}

MOCK_USER_2 = {
    'id': 2,
    'name': 'Daniel',
    'email': 'daniel@gmail.com',
    'identity_number': '01895142647',
    'password': 'batatinha2'
}

MOCK_WALLET_USER_1 = {
    'id': '8a504a8c-3fdc-4426-97bc-e4ebc50de011',
    'balance': Decimal(99.123),
    'user_id': MOCK_USER_1['id']
}

MOCK_WALLET_USER_2 = {
    'id': 'fbaf0d3f-8be2-40f2-b08e-56eaf0923ae8',
    'balance': Decimal(10.234),
    'user_id': MOCK_USER_1['id']
}

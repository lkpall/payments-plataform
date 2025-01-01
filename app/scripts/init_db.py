from sqlalchemy import text


CREATE_USER_TYPE = text("""
    INSERT INTO user_type (id, title)
    VALUES
            (1, 'Admin'),
            (2, 'Lojista'),
            (3, 'Consumidor')
    ON CONFLICT (id) DO NOTHING;
    """)

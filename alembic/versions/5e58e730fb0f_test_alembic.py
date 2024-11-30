"""test alembic

Revision ID: 5e58e730fb0f
Revises:
Create Date: 2024-11-29 15:37:36.894324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e58e730fb0f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'teste_alembic',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('teste_alembic')

"""Initial migration

Revision ID: 2045f4b56c07
Revises: f492e421ad6b
Create Date: 2024-07-03 09:19:44.661802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2045f4b56c07'
down_revision: Union[str, None] = 'f492e421ad6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('role_permissions', 'action')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role_permissions', sa.Column('action', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###

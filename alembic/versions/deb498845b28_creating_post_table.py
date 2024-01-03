"""creating post table

Revision ID: deb498845b28
Revises: 
Create Date: 2024-01-03 10:44:43.725067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'deb498845b28'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #creting the posts table logic:
    op.create_table('posts',
    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    #logic for downgrade:
    op.drop_table('posts')
    pass

"""add last few columns to posts

Revision ID: f93e9308a37b
Revises: 5fb9b9dfe374
Create Date: 2024-01-03 12:13:35.949499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f93e9308a37b'
down_revision: Union[str, None] = '5fb9b9dfe374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',
    sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('posts',
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)

    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass

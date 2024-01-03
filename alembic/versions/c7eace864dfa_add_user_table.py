"""add user table

Revision ID: c7eace864dfa
Revises: 29c206808441
Create Date: 2024-01-03 11:10:17.038493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7eace864dfa'
down_revision: Union[str, None] = '29c206808441'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
        # Create a table named "users"
    op.create_table(
        "users",
        # Column for user ID, an integer that cannot be null
        sa.Column("id", sa.Integer(), nullable=False),
        # Column for user email, a string that cannot be null
        sa.Column("email", sa.String(), nullable=False),
        # Column for user password, a string that cannot be null
        sa.Column("password", sa.String(), nullable=False),
        # Column for creation timestamp with timezone, defaulting to the current time
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        # Primary key constraint on the "id" column
        sa.PrimaryKeyConstraint('id'),
        # Unique constraint on the "email" column
        sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass

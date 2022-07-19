"""add user table

Revision ID: 748f1162a60f
Revises: a21ef0031af4
Create Date: 2022-07-18 21:09:29.725763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '748f1162a60f'
down_revision = 'a21ef0031af4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),  nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')

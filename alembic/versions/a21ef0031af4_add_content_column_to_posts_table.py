"""add content column to posts table

Revision ID: a21ef0031af4
Revises: 327a88ad7b21
Create Date: 2022-07-18 21:02:26.753190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a21ef0031af4'
down_revision = '327a88ad7b21'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')

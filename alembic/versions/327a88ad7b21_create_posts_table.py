"""create posts table

Revision ID: 327a88ad7b21
Revises: 
Create Date: 2022-07-18 20:51:37.851480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '327a88ad7b21'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )
    
    pass


def downgrade() -> None:
    pass

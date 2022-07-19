"""add last few columns to posts table

Revision ID: d922d1e54533
Revises: 530eaea4935e
Create Date: 2022-07-18 21:21:19.589550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd922d1e54533'
down_revision = '530eaea4935e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE')
    )
    
    op.add_column('posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
    )


def downgrade() -> None:
    op.drop_column('published')
    op.drop_column('created_at')

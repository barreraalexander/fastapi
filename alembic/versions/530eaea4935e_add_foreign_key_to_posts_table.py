"""add foreign key to posts table

Revision ID: 530eaea4935e
Revises: 748f1162a60f
Create Date: 2022-07-18 21:16:25.805116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '530eaea4935e'
down_revision = '748f1162a60f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')

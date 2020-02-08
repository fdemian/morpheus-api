"""Add date column to comments and stories

Revision ID: 1ce3e4dbb32f
Revises: e53e5a4e6213
Create Date: 2019-07-20 21:06:27.384635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ce3e4dbb32f'
down_revision = 'e53e5a4e6213'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('stories', sa.Column('date', sa.DateTime))
    op.add_column('comments', sa.Column('date', sa.DateTime))

def downgrade():
    op.drop_column('stories', sa.Column('date', sa.DateTime))
    op.drop_column('comments', sa.Column('date', sa.DateTime))

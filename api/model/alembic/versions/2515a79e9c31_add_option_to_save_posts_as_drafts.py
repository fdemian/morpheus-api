"""Add option to save posts as drafts.

Revision ID: 2515a79e9c31
Revises: 1ce3e4dbb32f
Create Date: 2019-10-19 16:17:43.105365

"""
from alembic import op
from sqlalchemy import Column, Boolean

# revision identifiers, used by Alembic.
revision = '2515a79e9c31'
down_revision = '1ce3e4dbb32f'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column('stories', Column('is_draft', Boolean, nullable=False, server_default='False'))

def downgrade():
  op.drop_column('stories', Column('is_draft', Boolean))

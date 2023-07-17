""" Add is_uploaded column to widget_documents table

Revision ID: df842dc6d0b7
Revises: 47fc88fe0477
Create Date: 2023-07-14 13:03:24.113767

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'df842dc6d0b7'
down_revision = '47fc88fe0477'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('widget_documents', sa.Column('is_uploaded', sa.Boolean(), nullable=False, server_default=sa.false()))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('widget_documents', 'is_uploaded')
    # ### end Alembic commands ###

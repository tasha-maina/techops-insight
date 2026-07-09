"""add next renewal date to customers

Revision ID: a7b4c2d1e8f9
Revises: ed6c0dc5fcbe
Create Date: 2026-07-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b4c2d1e8f9'
down_revision = 'ed6c0dc5fcbe'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('next_renewal_date', sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.drop_column('next_renewal_date')

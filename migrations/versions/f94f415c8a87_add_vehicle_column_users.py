"""add_vehicle_column_users

Revision ID: f94f415c8a87
Revises: 14630d2fc3d5
Create Date: 2023-05-22 16:53:34.408579

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'f94f415c8a87'
down_revision = '14630d2fc3d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('vehicle_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'users', 'vehicles', ['vehicle_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'vehicle_id')

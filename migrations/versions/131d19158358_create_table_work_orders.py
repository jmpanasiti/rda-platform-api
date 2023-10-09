"""create_table_work_orders

Revision ID: 131d19158358
Revises: a8b99f815fb2
Create Date: 2023-06-07 17:19:43.384399

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '131d19158358'
down_revision = 'a8b99f815fb2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_orders',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('status', sa.String(), nullable=False),
                    sa.Column('vehicle_id', sa.UUID(), nullable=False),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('is_deleted', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.alter_column('vehicles', 'registration_plate',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.create_index(op.f('ix_vehicles_registration_plate'),
                    'vehicles', ['registration_plate'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vehicles_registration_plate'),
                  table_name='vehicles')
    op.alter_column('vehicles', 'registration_plate',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.drop_table('work_orders')
    # ### end Alembic commands ###

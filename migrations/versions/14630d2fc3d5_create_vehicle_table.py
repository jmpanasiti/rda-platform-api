"""create vehicle table

Revision ID: 14630d2fc3d5
Revises: 035deeba3813
Create Date: 2023-05-22 16:30:22.962678

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '14630d2fc3d5'
down_revision = '035deeba3813'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('vehicles',
                    sa.Column('registration_plate',
                              sa.String(), nullable=False),
                    sa.Column('brand', sa.String(), nullable=False),
                    sa.Column('model', sa.String(), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=False),
                    sa.Column('fire_extinguisher_expiration_date',
                              sa.Date(), default=''),
                    sa.Column('vtv_expiration_date', sa.Date(), default=''),
                    sa.Column('documents_expiration_date',
                              sa.Date(), default=''),
                    sa.Column('next_service_date', sa.Date(), default=''),
                    sa.Column('policy_number', sa.String(), default=''),
                    # sa.Column('scoring_3s', sa.Integer(), default=''),
                    sa.Column('engraved_parts', sa.Boolean(), default=''),
                    sa.Column('policy_file', sa.String(), default='',),
                    sa.Column('id_card_file', sa.String(), default=''),
                    sa.Column('is_active', sa.Boolean(), default=True),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('is_deleted', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('vehicles')

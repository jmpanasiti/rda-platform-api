"""add agent to branches

Revision ID: 84e6fff65690
Revises: 21a62592bf2c
Create Date: 2023-09-22 10:13:21.582555

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '84e6fff65690'
down_revision = '21a62592bf2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('branches', sa.Column('agent_id', sa.UUID(), nullable=True))
    op.create_foreign_key('agent_fk', 'branches',
                          'users', ['agent_id'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('agent_fk', 'branches', type_='foreignkey')
    op.drop_column('branches', 'agent_id')
    # ### end Alembic commands ###

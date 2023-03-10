"""empty message

Revision ID: 224205ec18d2
Revises: fd8e57a932e8
Create Date: 2022-12-22 00:46:40.093027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '224205ec18d2'
down_revision = 'fd8e57a932e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eclients')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eclients',
    sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], name='eclients_client_id_fkey'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='eclients_event_id_fkey')
    )
    # ### end Alembic commands ###

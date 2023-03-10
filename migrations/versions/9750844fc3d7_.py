"""empty message

Revision ID: 9750844fc3d7
Revises: 59d7f6d811c6
Create Date: 2023-01-10 03:47:26.405266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9750844fc3d7'
down_revision = '59d7f6d811c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('eventready', schema=None) as batch_op:
        batch_op.drop_constraint('eventready_event_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('eventready_client_id_fkey', type_='foreignkey')
        batch_op.drop_column('client_id')
        batch_op.drop_column('event_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('eventready', schema=None) as batch_op:
        batch_op.add_column(sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('eventready_client_id_fkey', 'client', ['client_id'], ['id'])
        batch_op.create_foreign_key('eventready_event_id_fkey', 'event', ['event_id'], ['id'])

    # ### end Alembic commands ###

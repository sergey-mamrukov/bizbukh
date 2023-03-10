"""empty message

Revision ID: ed3b11e5854b
Revises: e1485c6b60ca
Create Date: 2023-02-11 01:48:52.041905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed3b11e5854b'
down_revision = 'e1485c6b60ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint('event_event_name_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_unique_constraint('event_event_name_key', ['event_name'])

    # ### end Alembic commands ###

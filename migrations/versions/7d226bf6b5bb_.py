"""empty message

Revision ID: 7d226bf6b5bb
Revises: a04cf81b43b9
Create Date: 2023-03-05 03:39:20.145684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d226bf6b5bb'
down_revision = 'a04cf81b43b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_column('client_dataavansa')
        batch_op.drop_column('client_datazp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_datazp', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('client_dataavansa', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###

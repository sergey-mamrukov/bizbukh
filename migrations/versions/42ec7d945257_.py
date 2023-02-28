"""empty message

Revision ID: 42ec7d945257
Revises: bfcebdb5ea80
Create Date: 2023-02-20 00:52:47.136855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42ec7d945257'
down_revision = 'bfcebdb5ea80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login', sa.Text(), nullable=True))
        batch_op.drop_column('email')
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('email', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_column('login')

    # ### end Alembic commands ###
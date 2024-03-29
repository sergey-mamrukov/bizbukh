"""empty message

Revision ID: 2823fb9d437d
Revises: bd381ec7a0ab
Create Date: 2023-03-14 00:24:19.015510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2823fb9d437d'
down_revision = 'bd381ec7a0ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_status', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_column('company_status')

    # ### end Alembic commands ###

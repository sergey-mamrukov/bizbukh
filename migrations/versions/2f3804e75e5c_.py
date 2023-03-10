"""empty message

Revision ID: 2f3804e75e5c
Revises: de735db5393b
Create Date: 2023-02-20 01:01:54.670903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f3804e75e5c'
down_revision = 'de735db5393b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('company_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['admin_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('company_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.drop_column('admin_id')

    # ### end Alembic commands ###

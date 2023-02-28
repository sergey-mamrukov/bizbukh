"""empty message

Revision ID: e4ffc7c55796
Revises: 2f3804e75e5c
Create Date: 2023-02-20 02:47:15.716133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4ffc7c55796'
down_revision = '2f3804e75e5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_constraint('company_admin_id_fkey', type_='foreignkey')
        batch_op.drop_column('admin_id')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'company', ['company_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('company_id')

    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('company_admin_id_fkey', 'user', ['admin_id'], ['id'])

    # ### end Alembic commands ###
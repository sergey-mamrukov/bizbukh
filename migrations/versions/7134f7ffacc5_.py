"""empty message

Revision ID: 7134f7ffacc5
Revises: ced960c2ecad
Create Date: 2022-12-13 01:51:19.663563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7134f7ffacc5'
down_revision = 'ced960c2ecad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nalogs',
    sa.Column('nalog_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['nalog_id'], ['systnalog.id'], )
    )
    with op.batch_alter_table('systnalog', schema=None) as batch_op:
        batch_op.drop_constraint('systnalog_client_id_fkey', type_='foreignkey')
        batch_op.drop_column('client_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('systnalog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('systnalog_client_id_fkey', 'client', ['client_id'], ['id'])

    op.drop_table('nalogs')
    # ### end Alembic commands ###

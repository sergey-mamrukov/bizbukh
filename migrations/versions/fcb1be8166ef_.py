"""empty message

Revision ID: fcb1be8166ef
Revises: 6629759e97f4
Create Date: 2023-01-10 05:57:16.096610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcb1be8166ef'
down_revision = '6629759e97f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('opfs')
    op.drop_table('nalogs')
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nalog_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('opf_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'systnalog', ['nalog_id'], ['id'])
        batch_op.create_foreign_key(None, 'opf', ['opf_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('opf_id')
        batch_op.drop_column('nalog_id')

    op.create_table('nalogs',
    sa.Column('nalog_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], name='nalogs_client_id_fkey'),
    sa.ForeignKeyConstraint(['nalog_id'], ['systnalog.id'], name='nalogs_nalog_id_fkey')
    )
    op.create_table('opfs',
    sa.Column('opf_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], name='opfs_client_id_fkey'),
    sa.ForeignKeyConstraint(['opf_id'], ['opf.id'], name='opfs_opf_id_fkey')
    )
    # ### end Alembic commands ###
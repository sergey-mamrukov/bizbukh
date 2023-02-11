"""empty message

Revision ID: d79ff308e76f
Revises: 88fe71dbcc4e
Create Date: 2023-01-23 03:25:48.128454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd79ff308e76f'
down_revision = '88fe71dbcc4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eventstatus')
    with op.batch_alter_table('eventready', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=80), nullable=True))
        batch_op.create_unique_constraint(None, ['status'])
        batch_op.drop_constraint('eventready_eventstatus_id_fkey', type_='foreignkey')
        batch_op.drop_column('eventstatus_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('eventready', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eventstatus_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('eventready_eventstatus_id_fkey', 'eventstatus', ['eventstatus_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('status')

    op.create_table('eventstatus',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status_name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='eventstatus_pkey'),
    sa.UniqueConstraint('status_name', name='eventstatus_status_name_key')
    )
    # ### end Alembic commands ###
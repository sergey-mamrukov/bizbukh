"""empty message

Revision ID: 88fe71dbcc4e
Revises: fcb1be8166ef
Create Date: 2023-01-11 00:33:46.943075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88fe71dbcc4e'
down_revision = 'fcb1be8166ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('evidotchet')
    op.drop_table('econtrolorgan')
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vidotchet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('controlorgan_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'vidotchet', ['vidotchet_id'], ['id'])
        batch_op.create_foreign_key(None, 'controlorgan', ['controlorgan_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('controlorgan_id')
        batch_op.drop_column('vidotchet_id')

    op.create_table('econtrolorgan',
    sa.Column('controlorgan_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['controlorgan_id'], ['controlorgan.id'], name='econtrolorgan_controlorgan_id_fkey'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='econtrolorgan_event_id_fkey')
    )
    op.create_table('evidotchet',
    sa.Column('vidotchet_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='evidotchet_event_id_fkey'),
    sa.ForeignKeyConstraint(['vidotchet_id'], ['vidotchet.id'], name='evidotchet_vidotchet_id_fkey')
    )
    # ### end Alembic commands ###

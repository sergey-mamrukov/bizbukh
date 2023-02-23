"""empty message

Revision ID: 28bd2d4e7d4e
Revises: 6db06bf22b1d
Create Date: 2023-02-22 03:58:10.723508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28bd2d4e7d4e'
down_revision = '6db06bf22b1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eusers',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    op.drop_table('eusers')
    # ### end Alembic commands ###

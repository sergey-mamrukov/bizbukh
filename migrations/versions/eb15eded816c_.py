"""empty message

Revision ID: eb15eded816c
Revises: a24d23b78da1
Create Date: 2023-02-16 04:43:55.390453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb15eded816c'
down_revision = 'a24d23b78da1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zarplata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.Text(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('data', sa.Date(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('zarplata')
    # ### end Alembic commands ###

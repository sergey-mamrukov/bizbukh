"""empty message

Revision ID: 6c3d3902fd13
Revises: 166f5504bde3
Create Date: 2023-01-10 04:23:49.334440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c3d3902fd13'
down_revision = '166f5504bde3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eventstatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eventstatus')
    # ### end Alembic commands ###

"""empty message

Revision ID: c00c55e213fd
Revises: 56a444db783b
Create Date: 2023-02-19 23:47:46.540941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c00c55e213fd'
down_revision = '56a444db783b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('b_company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('b_company')
    # ### end Alembic commands ###
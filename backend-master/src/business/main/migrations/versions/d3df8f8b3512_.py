"""empty message

Revision ID: d3df8f8b3512
Revises: bb0eb728327a
Create Date: 2019-03-04 11:11:00.884769

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd3df8f8b3512'
down_revision = 'bb0eb728327a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business_calculated_field', sa.Column('contain_function', sa.Boolean(), nullable=True))
    op.add_column('business_calculated_field', sa.Column('contain_group_function', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business_calculated_field', 'contain_group_function')
    op.drop_column('business_calculated_field', 'contain_function')
    # ### end Alembic commands ###
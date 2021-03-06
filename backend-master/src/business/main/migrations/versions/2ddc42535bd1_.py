"""empty message

Revision ID: 2ddc42535bd1
Revises: 70fc4a497980
Create Date: 2019-01-23 19:21:31.108696

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2ddc42535bd1'
down_revision = '70fc4a497980'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_segment',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('scope', sa.String(length=255), nullable=True),
    sa.Column('operation', sa.String(length=255), nullable=True),
    sa.Column('conditions', sa.Text(), nullable=True),
    sa.Column('space_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('ds_code', sa.String(length=50), nullable=False),
    sa.Column('connection_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['connection_id'], ['business_connection.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('business_segment')
    # ### end Alembic commands ###

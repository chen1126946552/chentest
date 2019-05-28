"""empty message

Revision ID: 2507af1b8eac
Revises: 
Create Date: 2019-01-10 00:29:21.201891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2507af1b8eac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_manager_connection',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('ds_code', sa.String(length=50), nullable=False),
    sa.Column('auth_type', sa.String(length=50), nullable=False),
    sa.Column('auth_info', sa.Text(), nullable=True),
    sa.Column('account_id', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data_manager_datasource',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=512), nullable=True),
    sa.Column('api_version', sa.String(length=50), nullable=False),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_manager_datasource')
    op.drop_table('data_manager_connection')
    # ### end Alembic commands ###

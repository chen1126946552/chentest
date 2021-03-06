"""empty message

Revision ID: 6c14666b7722
Revises: 6a694bb03cdc
Create Date: 2019-03-05 18:40:11.083651

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6c14666b7722'
down_revision = '6a694bb03cdc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_etl_datasource',
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated_at', sa.BigInteger(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('id', sa.String(length=47), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('fields', sa.Text(), nullable=True),
    sa.Column('time', sa.Text(), nullable=True),
    sa.Column('filters', sa.Text(), nullable=True),
    sa.Column('segment', sa.Text(), nullable=True),
    sa.Column('sort', sa.Text(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('space_id', sa.String(length=36), nullable=False),
    sa.Column('widget_connection_config_id', sa.String(length=50), nullable=False),
    sa.Column('language', sa.String(length=50), nullable=True),
    sa.Column('timezone', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_business_etl_datasource_space_id'), 'business_etl_datasource', ['space_id'], unique=False)
    op.create_index(op.f('ix_business_etl_datasource_widget_connection_config_id'), 'business_etl_datasource', ['widget_connection_config_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    op.drop_index(op.f('ix_business_etl_datasource_widget_connection_config_id'), table_name='business_etl_datasource')
    op.drop_index(op.f('ix_business_etl_datasource_space_id'), table_name='business_etl_datasource')
    op.drop_table('business_etl_datasource')
    # ### end Alembic commands ###

"""empty message

Revision ID: 6a694bb03cdc
Revises: 15e1b2b3bd95
Create Date: 2019-02-27 12:19:24.055815

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6a694bb03cdc'
down_revision = '15e1b2b3bd95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('business_access_rule', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_access_rule', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('business_access_rule', 'last_updated_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('business_connection', 'last_updated_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_file', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_file', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('business_connection_file', 'last_updated_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_filesheet', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_filesheet', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('business_connection_filesheet', 'last_updated_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_sheet', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_sheet', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('business_connection_sheet', 'last_updated_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_table', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_connection_table', 'dm_table_id',
               existing_type=mysql.VARCHAR(length=36),
               nullable=False)
    op.alter_column('business_connection_table', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('business_connection_table', 'last_updated_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_segment', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.alter_column('business_segment', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('business_segment', 'last_updated_at',
               existing_type=mysql.DATETIME(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('business_segment', 'last_updated_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_segment', 'is_deleted',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('business_segment', 'created_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_table', 'last_updated_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_table', 'is_deleted',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('business_connection_table', 'dm_table_id',
               existing_type=mysql.VARCHAR(length=36),
               nullable=True)
    op.alter_column('business_connection_table', 'created_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_sheet', 'last_updated_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_sheet', 'is_deleted',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('business_connection_sheet', 'created_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_filesheet', 'last_updated_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_filesheet', 'is_deleted',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('business_connection_filesheet', 'created_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_file', 'last_updated_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection_file', 'is_deleted',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('business_connection_file', 'created_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection', 'last_updated_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_connection', 'is_deleted',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('business_connection', 'created_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_access_rule', 'last_updated_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('business_access_rule', 'is_deleted',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('business_access_rule', 'created_at',
               existing_type=sa.BigInteger(),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    # ### end Alembic commands ###

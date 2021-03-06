"""empty message

Revision ID: a9e27c2a8462
Revises: 74eea112c7b4
Create Date: 2019-02-20 11:43:42.363945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9e27c2a8462'
down_revision = '74eea112c7b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_manager_table',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('connection_id', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('database', sa.String(length=512), nullable=False),
    sa.Column('columns', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['connection_id'], ['data_manager_connection.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_manager_table')
    # ### end Alembic commands ###

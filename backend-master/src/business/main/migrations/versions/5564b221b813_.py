"""empty message

Revision ID: 5564b221b813
Revises: d74c2dad7455
Create Date: 2019-03-22 19:19:34.107321

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5564b221b813'
down_revision = 'd74c2dad7455'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business_connection', sa.Column('ds_account_id', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business_connection', 'ds_account_id')
    # ### end Alembic commands ###

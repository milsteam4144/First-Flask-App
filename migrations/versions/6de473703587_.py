"""empty message

Revision ID: 6de473703587
Revises: 9858cde0a04a
Create Date: 2018-12-12 18:32:03.480951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6de473703587'
down_revision = '9858cde0a04a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('title', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'title')
    # ### end Alembic commands ###

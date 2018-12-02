"""empty message

Revision ID: 69f19e9d3042
Revises: c25922957168
Create Date: 2018-12-02 23:27:50.468418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69f19e9d3042'
down_revision = 'c25922957168'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
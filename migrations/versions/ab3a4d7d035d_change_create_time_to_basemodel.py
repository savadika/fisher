"""change create_time to baseModel

Revision ID: ab3a4d7d035d
Revises: adeda0a82566
Create Date: 2019-02-22 16:45:54.509499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab3a4d7d035d'
down_revision = 'adeda0a82566'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('create_time', sa.String(length=200), nullable=False))
    op.add_column('user', sa.Column('create_time', sa.String(length=200), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'create_time')
    op.drop_column('book', 'create_time')
    # ### end Alembic commands ###

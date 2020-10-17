"""empty message

Revision ID: a524f430c1ad
Revises: d7265ec332c2
Create Date: 2020-10-17 00:58:33.704575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a524f430c1ad'
down_revision = 'd7265ec332c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('class1', sa.String(length=120), nullable=True))
    op.add_column('products', sa.Column('department', sa.String(length=120), nullable=True))
    op.add_column('products', sa.Column('subclass1', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'subclass1')
    op.drop_column('products', 'department')
    op.drop_column('products', 'class1')
    # ### end Alembic commands ###

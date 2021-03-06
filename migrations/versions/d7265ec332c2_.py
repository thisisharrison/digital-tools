"""empty message

Revision ID: d7265ec332c2
Revises: 3297dd286f73
Create Date: 2020-10-17 00:57:22.431405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7265ec332c2'
down_revision = '3297dd286f73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'class1')
    op.drop_column('products', 'subclass1')
    op.drop_column('products', 'department')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('department', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('subclass1', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('class1', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

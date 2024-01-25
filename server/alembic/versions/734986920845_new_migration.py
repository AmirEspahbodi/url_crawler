"""New Migration

Revision ID: 734986920845
Revises: 556f863b8212
Create Date: 2024-01-24 22:44:21.900755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '734986920845'
down_revision = '556f863b8212'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###

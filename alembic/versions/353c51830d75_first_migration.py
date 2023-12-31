"""First migration

Revision ID: 353c51830d75
Revises: 
Create Date: 2023-07-27 22:34:00.341542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '353c51830d75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('uid', sa.String(), nullable=True),
    sa.Column('displayName', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('photoURL', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

"""empty message

Revision ID: 042fe98bc515
Revises: fba5b6b63975
Create Date: 2019-12-15 02:55:14.731577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '042fe98bc515'
down_revision = 'fba5b6b63975'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('coins')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coins',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('token', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='coins_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='coins_pkey')
    )
    # ### end Alembic commands ###
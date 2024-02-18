"""User password update

Revision ID: 201bc396531d
Revises: e6f3053e9f4e
Create Date: 2024-02-18 18:34:05.094760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '201bc396531d'
down_revision = 'e6f3053e9f4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=102),
               type_=sa.VARCHAR(length=162),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=162),
               type_=sa.VARCHAR(length=102),
               existing_nullable=False)

    # ### end Alembic commands ###

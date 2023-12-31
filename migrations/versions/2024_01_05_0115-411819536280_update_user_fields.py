"""update_user_fields

Revision ID: 411819536280
Revises: 747eb5bc99eb
Create Date: 2024-01-05 01:15:07.564557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '411819536280'
down_revision: str|None = '747eb5bc99eb'
branch_labels: str|None = None
depends_on: str|None = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.alter_column('public_key',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.alter_column('private_key',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.alter_column('private_key',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
        batch_op.alter_column('public_key',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###

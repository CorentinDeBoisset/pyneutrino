"""Add invite_code on conversations

Revision ID: 195c70528b47
Revises: 4ffd424766cb
Create Date: 2024-01-06 19:04:35.866022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '195c70528b47'
down_revision: str | None = '4ffd424766cb'
branch_labels: str | None = None
depends_on: str | None = None


def upgrade():
    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('invite_code', sa.VARCHAR(), nullable=True))
        batch_op.create_index(batch_op.f('ix_conversation_invite_code'), ['invite_code'], unique=True)
        batch_op.drop_column('reveiver_public_key')


def downgrade():
    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reveiver_public_key', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_index(batch_op.f('ix_conversation_invite_code'))
        batch_op.drop_column('invite_code')

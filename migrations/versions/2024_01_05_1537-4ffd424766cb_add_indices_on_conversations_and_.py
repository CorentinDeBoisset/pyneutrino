"""Add indices on conversations and messages

Revision ID: 4ffd424766cb
Revises: a6936caa2ede
Create Date: 2024-01-05 15:37:39.949827

"""
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4ffd424766cb'
down_revision: str | None = 'a6936caa2ede'
branch_labels: str | None = None
depends_on: str | None = None


def upgrade():
    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.alter_column(
            'creation_date',
            existing_type=postgresql.TIMESTAMP(),
            nullable=False
        )
        batch_op.alter_column(
            'last_update_date',
            existing_type=postgresql.TIMESTAMP(),
            nullable=False
        )
        batch_op.create_index(batch_op.f('ix_conversation_last_update_date'), ['last_update_date'], unique=False)

    with op.batch_alter_table('sent_message', schema=None) as batch_op:
        batch_op.create_index('ix_conversation_message_order', ['conversation_id', 'creation_date'], unique=False)


def downgrade():
    with op.batch_alter_table('sent_message', schema=None) as batch_op:
        batch_op.drop_index('ix_conversation_message_order')

    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_conversation_last_update_date'))
        batch_op.alter_column(
            'last_update_date',
            existing_type=postgresql.TIMESTAMP(),
            nullable=True
        )
        batch_op.alter_column(
            'creation_date',
            existing_type=postgresql.TIMESTAMP(),
            nullable=True
        )

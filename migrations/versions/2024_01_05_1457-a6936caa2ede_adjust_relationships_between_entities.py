"""Adjust relationships between entities

Revision ID: a6936caa2ede
Revises: 6a60c2887c98
Create Date: 2024-01-05 14:57:11.974120

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a6936caa2ede'
down_revision: str | None = '6a60c2887c98'
branch_labels: str | None = None
depends_on: str | None = None


def upgrade():
    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.drop_constraint('conversation_creator_fkey', type_='foreignkey')
        batch_op.drop_constraint('conversation_receiver_fkey', type_='foreignkey')
        batch_op.alter_column('creator', new_column_name='creator_id')
        batch_op.alter_column('receiver', new_column_name='receiver_id')
        batch_op.create_foreign_key('created_conversations_fkey', 'user_account', ['creator_id'], ['id'])
        batch_op.create_foreign_key('received_conversation_fkey', 'user_account', ['receiver_id'], ['id'])

    with op.batch_alter_table('sent_message', schema=None) as batch_op:
        batch_op.drop_constraint('sent_message_conversation_fkey', type_='foreignkey')
        batch_op.alter_column('conversation', new_column_name='conversation_id')
        batch_op.create_foreign_key('conversation_fkey', 'conversation', ['conversation_id'], ['id'])


def downgrade():
    with op.batch_alter_table('sent_message', schema=None) as batch_op:
        batch_op.drop_constraint('conversation_fkey', type_='foreignkey')
        batch_op.alter_column('conversation_id', new_column_name='conversation')
        batch_op.create_foreign_key('sent_message_conversation_fkey', 'conversation', ['conversation'], ['id'])

    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.drop_constraint('received_conversation_fkey', type_='foreignkey')
        batch_op.drop_constraint('created_conversations_fkey', type_='foreignkey')
        batch_op.alter_column('receiver_id', new_column_name='receiver')
        batch_op.alter_column('creator_id', new_column_name='creator')
        batch_op.create_foreign_key('conversation_receiver_fkey', 'user_account', ['receiver'], ['id'])
        batch_op.create_foreign_key('conversation_creator_fkey', 'user_account', ['creator'], ['id'])

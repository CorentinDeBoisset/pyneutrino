"""make usernames nullable

Revision ID: 62dce14e12c2
Revises: 195c70528b47
Create Date: 2024-01-08 17:59:18.748984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62dce14e12c2"
down_revision: str | None = "195c70528b47"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade():
    with op.batch_alter_table("user_account", schema=None) as batch_op:
        batch_op.alter_column("username", existing_type=sa.VARCHAR(), nullable=True)


def downgrade():
    with op.batch_alter_table("user_account", schema=None) as batch_op:
        batch_op.alter_column("username", existing_type=sa.VARCHAR(), nullable=False)

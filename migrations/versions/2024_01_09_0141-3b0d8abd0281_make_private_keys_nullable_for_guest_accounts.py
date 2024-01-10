"""Make private_keys nullable for guest accounts

Revision ID: 3b0d8abd0281
Revises: 62dce14e12c2
Create Date: 2024-01-09 01:41:31.054702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3b0d8abd0281"
down_revision: str | None = "62dce14e12c2"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade():
    op.alter_column("user_account", "private_key", existing_type=sa.TEXT(), nullable=True)


def downgrade():
    op.alter_column("user_account", "private_key", existing_type=sa.TEXT(), nullable=False)

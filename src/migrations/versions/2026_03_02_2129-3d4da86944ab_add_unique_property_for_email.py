"""add unique property for email

Revision ID: 3d4da86944ab
Revises: ed34a983ba1b
Create Date: 2026-03-02 21:29:07.386826

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d4da86944ab"
down_revision: Union[str, Sequence[str], None] = "ed34a983ba1b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")  # type: ignore

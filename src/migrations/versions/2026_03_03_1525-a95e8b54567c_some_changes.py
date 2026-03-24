"""some changes

Revision ID: a95e8b54567c
Revises: 3d4da86944ab
Create Date: 2026-03-03 15:25:55.091689

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "a95e8b54567c"
down_revision: Union[str, Sequence[str], None] = "3d4da86944ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

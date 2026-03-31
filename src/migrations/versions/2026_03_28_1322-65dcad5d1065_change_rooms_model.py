"""change rooms model

Revision ID: 65dcad5d1065
Revises: 113791ee228c
Create Date: 2026-03-28 13:22:59.591807

"""

from typing import Sequence, Union

revision: str = "65dcad5d1065"
down_revision: Union[str, Sequence[str], None] = "113791ee228c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass


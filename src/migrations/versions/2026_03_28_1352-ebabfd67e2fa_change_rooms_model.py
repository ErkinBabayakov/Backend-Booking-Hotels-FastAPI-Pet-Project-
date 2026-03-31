"""change rooms model

Revision ID: ebabfd67e2fa
Revises: 65dcad5d1065
Create Date: 2026-03-28 13:52:37.052320

"""

from typing import Sequence, Union

from alembic import op

revision: str = "ebabfd67e2fa"
down_revision: Union[str, Sequence[str], None] = "65dcad5d1065"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("rooms_facilities_room_id_fkey"), "rooms_facilities", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "rooms_facilities", "rooms", ["room_id"], ["id"], ondelete="CASCADE"
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_facilities_room_id_fkey"),
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
    )


from datetime import date
from sqlalchemy import ForeignKey, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import Base


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    price: Mapped[int]
    date_from: Mapped[date]
    date_to: Mapped[date]
    created_at: Mapped[DateTime] = Column(DateTime, server_default=func.now(timezone=True))



    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days



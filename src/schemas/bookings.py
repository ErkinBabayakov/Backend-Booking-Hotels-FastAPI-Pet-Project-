from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int

class BookingAdd(BaseModel):
    room_id: int
    user_id: int
    price: int
    date_from: date
    date_to:date
    created_at: datetime


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
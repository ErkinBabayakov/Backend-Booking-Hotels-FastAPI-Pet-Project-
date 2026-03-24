from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BaseModel):
    room_id: int
    user_id: int
    price: int
    date_from: date
    date_to: date


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

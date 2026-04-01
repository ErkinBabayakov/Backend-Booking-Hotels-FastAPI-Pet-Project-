from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование номера"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me", summary="Получить только мои бронирования")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_me(user_id=user_id)


@router.post("", summary="Добавить бронирование")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest = Body()):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}

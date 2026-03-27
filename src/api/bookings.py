from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирование номера"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получить только мои бронирования")
async def get_me(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return bookings


@router.post("", summary="Добавить бронирование")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest = Body()):
    # Получаем цену номера
    try:
        room: Room | None = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price

    # Создаем схему данных BookingAdd
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())

    # Добавляем бронирование конкретному пользователю
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}

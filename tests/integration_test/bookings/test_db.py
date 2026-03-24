from datetime import date

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        price=1000,
        date_from=date(year=2026, month=5, day=7),
        date_to=date(year=2026, month=5, day=12),
    )
    # Создаем бронь
    new_booking = await db.bookings.add(booking_data)

    # Получаем бронь и проверяем существует ли она
    get_booking_data = await db.bookings.get_one_or_none(id=new_booking.id)
    assert get_booking_data
    assert get_booking_data.id == new_booking.id
    assert get_booking_data.room_id == new_booking.room_id
    assert get_booking_data.user_id == new_booking.user_id
    assert get_booking_data.price == new_booking.price
    assert get_booking_data.date_from == new_booking.date_from
    assert get_booking_data.date_to == new_booking.date_to

    # Обновляем бронь
    update_date = date(year=2026, month=5, day=15)
    update_booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        price=1000,
        date_from=date(year=2026, month=5, day=7),
        date_to=update_date,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.room_id == new_booking.room_id
    assert updated_booking.user_id == new_booking.user_id

    # Удаляем бронь
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking

    await db.commit()

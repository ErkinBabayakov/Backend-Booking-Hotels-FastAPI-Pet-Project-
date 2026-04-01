import pytest
from httpx import AsyncClient

from src.utils.db_manager import DBManager
from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-08-01", "2026-09-01", 200),
        (1, "2026-08-02", "2026-09-02", 200),
        (1, "2026-08-03", "2026-09-03", 200),
        (1, "2026-08-04", "2026-09-04", 200),
        (1, "2026-08-05", "2026-09-05", 200),
        (1, "2026-08-06", "2026-09-06", 409),
        (1, "2026-09-07", "2026-09-10", 200),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db: DBManager, authenticated_ac: AsyncClient
):
    # room_id = (await db.rooms.get_all())[0].id
    await authenticated_ac.post("/auth/login", json={"email": "kot1@pes.com", "password": "1234"})
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert res["data"]["room_id"] == room_id
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_booking():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2026-08-01", "2026-09-01", 1),
        (1, "2026-08-02", "2026-09-02", 2),
        (1, "2026-08-03", "2026-09-03", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    authenticated_ac: AsyncClient,
    delete_all_booking,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    response_booking = await authenticated_ac.get("/bookings/me")
    assert len(response_booking.json()) == booked_rooms
    assert response_booking.status_code == 200

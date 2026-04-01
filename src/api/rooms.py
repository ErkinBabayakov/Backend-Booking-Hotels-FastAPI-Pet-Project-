from datetime import date
from fastapi import APIRouter, Body, Query

from src.exceptions import RoomNotFoundException, RoomNotFoundHTTPException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.services.hotels import HotelService
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2026-08-01"),
    date_to: date = Query(example="2026-08-10"),
):
    return await RoomService(db).get_rooms(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms{room_id}", summary="Получить номер отеля")
async def get_room(db: DBDep, room_id: int, hotel_id: int):
    try:
        return await RoomService(db).get_room(room_id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Создать номер отеля")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    await HotelService(db).get_hotel_with_check(hotel_id)
    room = await RoomService(db).create_room(hotel_id, room_data)
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить информацию о номере")
async def update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    await RoomService(db).update_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить информацию о номере")
async def partial_update_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    await RoomService(db).partial_update_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}

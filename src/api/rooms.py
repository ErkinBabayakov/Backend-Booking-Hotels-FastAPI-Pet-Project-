from fastapi import APIRouter, Body
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])

@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(db:DBDep, hotel_id:int):
    return await db.rooms.get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms{room_id}", summary="Получить номер отеля")
async def get_rooms(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Создать номер отеля")
async def create_room(db: DBDep, hotel_id: int ,room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms", summary="Обновить информацию о номере")
async def update_room(db: DBDep, hotel_id:int, room_id:int, room_data: RoomAddRequest):
    await db.rooms.edit(room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить информацию о номере")
async def partial_update_room(db: DBDep, hotel_id:int, room_id:int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DBDep, hotel_id:int, room_id:int):
    await db.rooms.delete(hotel_id=hotel_id ,id=room_id)
    await db.commit()
    return {"status": "OK"}
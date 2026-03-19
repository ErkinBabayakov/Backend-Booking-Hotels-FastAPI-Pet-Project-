from datetime import date
from fastapi import APIRouter, Body, Query

from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])

@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(db:DBDep,
                    hotel_id:int,
                    date_from:date = Query(examples="2026-08-01"),
                    date_to: date = Query(examples="2026-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms{room_id}", summary="Получить номер отеля")
async def get_rooms(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none_with_rels(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Создать номер отеля")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    room_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.room_facility.add_bulk(room_facilities_data)

    await db.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновить информацию о номере")
async def update_room(db: DBDep, hotel_id:int, room_id:int, room_data: RoomAddRequest):

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, id=room_id)

    await db.room_facility.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить информацию о номере")
async def partial_update_room(db: DBDep, hotel_id:int, room_id:int, room_data: RoomPatchRequest):

    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in  _room_data_dict:
        await db.room_facility.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DBDep, hotel_id:int, room_id:int):
    await db.rooms.delete(hotel_id=hotel_id ,id=room_id)
    await db.commit()
    return {"status": "OK"}
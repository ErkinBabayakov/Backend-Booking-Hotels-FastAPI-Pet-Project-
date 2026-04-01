from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить данные об отеле")
@cache(expire=30)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(default=None, description="Отель"),
    date_from: date = Query(examples="2026-08-01"),
    date_to: date = Query(examples="2026-08-10"),
):
    return await HotelService(db).get_hotels(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}", summary="Получить отель по его id")
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException


@router.post("", summary="Создаем отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "" "summary": "Сочи",
                "value": {"title": "Отель Сочи 5 звезд у моря", "location": "ул.Моря, 1"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Отель Дубай у Бурдж-Халиф", "location": "ул.Шейха, 3"},
            },
        }
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление информации об отеле")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).update_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("{hotel_id}", summary="Частичное обновление информации об отеле")
async def partial_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await HotelService(db).partial_update_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/hotel_id", summary="Удаляем отель")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}

from datetime import date
from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить данные об отеле")
@cache(expire=30)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(default=None, description="Отель"),
        date_from: date = Query(example="2026-08-01"),
        date_to: date = Query(example="2026-08-10")
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )




@router.post("", summary="Создаем отель")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {""
          "summary": "Сочи",
          "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул.Моря, 1"
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
        "title": "Отель Дубай у Бурдж-Халиф",
        "location": "ул.Шейха, 3"
        }
    }
})):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}

@router.put("/{hotel_id}", summary="Полное обновление информации об отеле")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch("{hotel_id}", summary="Частичное обновление информации об отеле")
async def partial_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):

    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.get("/{hotel_id}", summary="Получить отель по его id")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.delete("/hotel_id", summary="Удаляем отель")
async def delete_hotel(db: DBDep, hotel_id: int):

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}

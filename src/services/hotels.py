from datetime import date
from typing import List

from src.api.dependencies import PaginationDep
from src.exceptions import check_date_to_after_date_from, HotelNotFoundException, ObjectNotFoundException
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
            self,
            pagination: PaginationDep,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date
) -> List[Hotel]:
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5

        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int) -> Hotel:
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        hotel = await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()
        return hotel

    async def partial_update_hotel(self, hotel_id: int, hotel_data: HotelPATCH):
        hotel = await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        return hotel

    async def get_hotel_with_check(self, hotel_id: int) -> None:
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
from src.tasks.tasks import test_task

from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facility(self, facility_data: FacilityAdd):
        facilities = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()
        return facilities
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства/Услуги"])


@router.get("", summary="Получить услуги")
@cache(expire=20)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("", summary="Создать услугу")
async def add_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facilities = await FacilityService(db).add_facility(facility_data)
    return {"status": "ok", "facilities": facilities}

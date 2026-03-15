from fastapi_cache.decorator import cache

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep

from src.schemas.facilities import  FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства/Услуги"])

@router.get("", summary="Получить услуги")
@cache(expire=20)
async def get_facilities(db:DBDep):
    print("ИДУ В БАЗУ ДАННЫХ")
    return await db.facilities.get_all()


@router.post("", summary="Создать услугу")
async def add_facility(db:DBDep, facility_data: FacilityAdd = Body()):
    facilities = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "ok", "facilities": facilities}
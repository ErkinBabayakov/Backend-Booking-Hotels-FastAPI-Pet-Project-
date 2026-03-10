from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facilities import  FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства/Услуги"])

@router.get("", summary="Получить услуги")
async def get_facilities(db:DBDep):
    return await db.facilities.get_all()

@router.post("", summary="Создать услугу")
async def add_facility(db:DBDep, facility_data: FacilityAdd = Body()):
    facilities = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "ok", "facilities": facilities}
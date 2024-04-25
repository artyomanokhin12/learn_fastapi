from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRoom

router = APIRouter(
    prefix='/hotels',
    tags = ['Действия с отелями'],
)

@router.get('/{hotel_id}/rooms')
async def get_all_hotel_rooms(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
    ) -> list[SRoom]:
    rooms = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    return rooms
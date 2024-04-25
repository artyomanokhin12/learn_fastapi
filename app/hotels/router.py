from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.schemas import SHotelInfo, SHotelsList
from app.hotels.dao import HotelDAO

router = APIRouter(
    prefix='/hotels',
    tags=['Действия с отелями'],
)

@router.get("/{location}")
async def find_hotel_by_location(
    location: str, 
    date_from: date = Query(..., description=f'Например, {datetime.now().date()}'), 
    date_to: date = Query(..., description=f'Например, {(datetime.now() + timedelta(days=14)).date()}')
    ) -> List[SHotelsList]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31: 
        raise CannotBookHotelForLongPeriod
    hotels_list = await HotelDAO.hotels_list(location=location, date_from=date_from, date_to=date_to)
    return hotels_list


@router.get('/id/{hotel_id}')
async def find_hotel(hotel_id: int) -> Optional[SHotelInfo]:
    result = await HotelDAO.find_by_id(hotel_id)
    return result
from datetime import date
from fastapi import APIRouter, Depends, HTTPException

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post("")
async def add_bookinig(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return "Вы забронировали комнату"
    

@router.delete('/{booking_id}')
async def delete_booking(booking_id: int, user:Users = Depends(get_current_user)):
    await BookingDAO.delete(user_id=user.id, id=booking_id)
    return "Вы удалили бронирование комнаты"
    
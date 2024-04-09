from fastapi import APIRouter, Request

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user):
    pass
    
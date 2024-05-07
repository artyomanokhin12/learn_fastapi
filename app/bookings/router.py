from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from sqlalchemy import inspect

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings
from app.exceptions import (IncorrectDateSet, LargePeriodError,
                            RoomCannotBeBooked)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


def obj_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post("")
async def add_bookinig(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    if (date_to - date_from).days < 0:
        raise IncorrectDateSet
    elif (date_to - date_from).days > 30:
        raise LargePeriodError
    else:
        booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
        if not booking:
            raise RoomCannotBeBooked
        booking_json = (
            TypeAdapter(SBookings).validate_python(obj_to_dict(booking)).model_dump()
        )
        send_booking_confirmation_email.delay(booking_json, user.email)
        return booking_json


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.delete(user_id=user.id, id=booking_id)
    return "Вы удалили бронирование комнаты"

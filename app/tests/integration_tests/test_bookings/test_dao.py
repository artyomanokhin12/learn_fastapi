from app.bookings.dao import BookingDAO
from datetime import datetime


async def test_add_and_get_new_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=3,
        date_from=datetime.strptime("2023-07-05", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-15", "%Y-%m-%d")
    )

    # print(new_booking)

    assert new_booking.user_id == 2
    assert new_booking.room_id == 3

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None

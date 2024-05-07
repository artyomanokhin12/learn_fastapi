from datetime import datetime

from app.bookings.dao import BookingDAO

# async def test_add_and_get_new_booking():
#     new_booking = await BookingDAO.add(
#         user_id=2,
#         room_id=3,
#         date_from=datetime.strptime("2023-07-05", "%Y-%m-%d"),
#         date_to=datetime.strptime("2023-07-15", "%Y-%m-%d")
#     )

#     assert new_booking.user_id == 2
#     assert new_booking.room_id == 3

#     new_booking = await BookingDAO.find_by_id(new_booking.id)

#     assert new_booking is not None


async def test_crud_bookings():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=4,
        date_from=datetime.strptime("2023-07-05", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-15", "%Y-%m-%d")
    )

    assert new_booking.id == 4
    read_booking = await BookingDAO.find_by_id(new_booking.id)
    assert read_booking is not None
    await BookingDAO.delete(id=new_booking.id)
    read_booking = await BookingDAO.find_by_id(new_booking.id)
    assert read_booking is None


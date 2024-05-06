from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("room_id,date_from,date_to,status_code,booked_rooms", [
    (4, "2030-05-01", "2030-05-15", 200, 3),
    (4, "2030-05-01", "2030-05-15", 200, 4),
    (4, "2030-05-01", "2030-05-15", 200, 5),
    (4, "2030-05-01", "2030-05-15", 200, 6),
    (4, "2030-05-01", "2030-05-15", 200, 7),
    (4, "2030-05-01", "2030-05-15", 200, 8),
    (4, "2030-05-01", "2030-06-15", 400, 8),
    (4, "2030-06-01", "2030-05-15", 400, 8),
    (4, "2030-05-01", "2030-05-15", 200, 9),
    (4, "2030-05-01", "2030-05-15", 200, 10),
    (4, "2030-05-01", "2030-05-15", 409, 10),
    (4, "2030-05-01", "2030-05-15", 409, 10),
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code, booked_rooms, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms
    

async def test_get_and_delete_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")

    bookings = [bookings["id"] for bookings in response.json()]

    for booking_id in bookings:
        await authenticated_ac.delete(f"/bookings/{booking_id}")

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == 0

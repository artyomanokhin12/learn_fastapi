from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router=router_users)
app.include_router(router=router_bookings)


class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            has_spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=1, gl=5)
     ) -> None:
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SHotels(BaseModel):
    adress: str
    name: str
    stars: str

@app.get("/hotels/{hotels_id}", response_model=list[SHotels])
def get_hotels(search_args: HotelsSearchArgs = Depends()) -> list[SHotels]:
    hotels = [
        {
            'adress': 'Baker Street, 221B',
            'name': 'Sherlock Holmes',
            'stars': '5'
        },
    ]
    return hotels

class SBooking(BaseModel):
    room_id: int
    date_from: int
    date_to: int


@app.post("/booking")
def add_booking(booking: SBooking):
    pass

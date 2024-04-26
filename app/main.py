from datetime import date
from typing import Optional

from fastapi import Depends, FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotel
from app.hotels.rooms.router import router as router_rooms

from app.pages.router import router as router_pages
from app.images.router import router as router_images

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router=router_users)
app.include_router(router=router_bookings)
app.include_router(router=router_hotel)
app.include_router(router=router_rooms)

app.include_router(router_pages)
app.include_router(router_images)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешили домены, с которых можно делать обращение к нашему API
    allow_credentials=True, # Разрешает делать куки, и, если включено, при каждом запросе посылает куки. Если не включено - не сможем распознать, кто к нам пришел
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"], # Разрешает методы, которые применимы к API
    allow_headers=["Content-type", "Set-Cookie", 
                   "Access-Control-Allow-Headers", "Access-Authorizations"], # Разрешает заголовки, применимые к нашему API 
)

# Пример написания эндпоинта со всеми моментами
#
#
# class HotelsSearchArgs:
#     def __init__(
#             self,
#             location: str,
#             date_from: date,
#             date_to: date,
#             has_spa: Optional[bool] = None,
#             stars: Optional[int] = Query(None, ge=1, gl=5)
#      ) -> None:
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars


# class SHotels(BaseModel):
#     adress: str
#     name: str
#     stars: str

# @app.get("/hotels/{hotels_id}", response_model=list[SHotels])
# def get_hotels(search_args: HotelsSearchArgs = Depends()) -> list[SHotels]:
#     hotels = [
#         {
#             'adress': 'Baker Street, 221B',
#             'name': 'Sherlock Holmes',
#             'stars': '5'
#         },
#     ]
#     return hotels

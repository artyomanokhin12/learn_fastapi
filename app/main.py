from contextlib import asynccontextmanager
import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from prometheus_fastapi_instrumentator import Instrumentator
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotel
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


sentry_sdk.init(
    dsn="https://0ea5d4ff8b763c00edccb38186d89ad5@o4507250444861440.ingest.de.sentry.io/4507250450825296",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


app = FastAPI(lifespan=lifespan)

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

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")



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

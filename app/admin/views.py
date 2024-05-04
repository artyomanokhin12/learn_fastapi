from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password] # данной строкой мы убрали показ в детальной информации по пользователю его хэшированного пароля
    can_delete = False  # Этой строкой мы убрали возможность удаления пользователя 
    name = "Пользователи"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]  # Чтобы не перечислять все колонки через запятую, мы получим их название с помощью цикла
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"

class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"

class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.bookings, Rooms.hotels]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


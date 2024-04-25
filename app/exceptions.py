from fastapi import HTTPException, status


class BookingExceptions(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingExceptions):
    status_code=status.HTTP_409_CONFLICT
    detail='Пользователь уже существует'


class IncorrectEmailOrPasswordException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Неверная почта или пароль'


class TokenExpiredException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Токен истек'


class TokenAbsentException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Токен отсутствует'


class IncorrectTokenFormatException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Неверный формат токена'


class UserIsNotPresentException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingExceptions):
    status_code=status.HTTP_409_CONFLICT
    detail='Не осталось свободных комнат'


class DateFromCannotBeAfterDateTo(BookingExceptions):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Дата заезда не может быть позже даты выезда"


class CannotBookHotelForLongPeriod(BookingExceptions):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Невозможно забронировать отель сроком более месяца"



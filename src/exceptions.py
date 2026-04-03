from datetime import date
from fastapi import HTTPException, status


class BronirovanieException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BronirovanieException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class AllRoomsAreBookedException(BronirovanieException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(BronirovanieException):
    detail = "Объект уже существует"


class IncorrectTokenException(BronirovanieException):
    detail = "Неверный токен"


class EmailNotRegisteredException(BronirovanieException):
    detail = "Пользователь с таким email не зарегистрирован"

class EmailNotCorrectException(BronirovanieException):
    detail = "Неправильно введён email. Введите корректный email"


class IncorrectPasswordException(BronirovanieException):
    detail = "Неверный пароль"


class UserAlreadyExistsException(BronirovanieException):
    detail = "Пользователь с таким email уже сущесвует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Дата заезда не может быть равна или позже даты выезда",
        )


class BronirovanieHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BronirovanieHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BronirovanieHTTPException):
    status_code = 404
    detail = "Номер не найден"


class UserNotFoundHTTPException(BronirovanieHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class AllRoomsAreBookedHTTPException(BronirovanieHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(BronirovanieHTTPException):
    status_code = 401
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(BronirovanieHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(BronirovanieHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class IncorrectPasswordHTTPException(BronirovanieHTTPException):
    status_code = 401
    detail = "Неверный пароль"


class NoAccessTokenHTTPException(BronirovanieHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"

class EmailNotCorrectHTTPException(BronirovanieHTTPException):
    status_code = 401
    detail = "Неправильно введён email. Введите корректный email"



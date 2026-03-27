from datetime import date
from fastapi import HTTPException, status

class BronirovanieException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(BronirovanieException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(BronirovanieException):
    detail = "Не осталось свободных номеров"

class ObjectIsExistsException(BronirovanieException):
    detail = "Объект уже существует"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                        detail="Дата заезда не может быть позже даты выезда")


class BronirovanieHTTPException(Exception):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundException(BronirovanieHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundException(BronirovanieHTTPException):
    status_code = 404
    detail = "Номер не найден"
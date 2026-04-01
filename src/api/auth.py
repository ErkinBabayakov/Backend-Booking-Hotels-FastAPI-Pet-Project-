from fastapi import APIRouter, Response

from src.exceptions import (
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    UserNotFoundHTTPException,
    UserNotFoundException,
)
from src.services.auth import AuthService
from src.schemas.users import UserRequestAdd
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Создать пользователя")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    return {"status": "OK"}


@router.post("/login", summary="Войти")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Мой профиль")
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        return await AuthService(db).get_me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post("/logout", summary="Выйти")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.delete("/{user_id}", summary="Удаляем пользователя с бд")
async def user_delete(db: DBDep, user_id: int):
    await AuthService(db).delete_user(user_id)
    return {"status": "OK"}

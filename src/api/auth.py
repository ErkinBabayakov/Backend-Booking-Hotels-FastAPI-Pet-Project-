from fastapi import APIRouter, HTTPException, status, Response

from src.exceptions import ObjectIsExistsException
from src.services.auth import AuthService
from src.schemas.users import UserRequestAdd, UserAdd
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Создать пользователя")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

        await db.users.add(new_user_data)
        await db.commit()
    except ObjectIsExistsException:  # noqa: E722
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email уже сущестует")
    return {"status": "ok"}


@router.post("/login", summary="Войти")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    user = await db.users.get_user_with_hash_password(email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким email не существует",
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получить данные о пользователе")
async def get_me(db: DBDep, user_id: UserIdDep):
    _user = await db.users.get_one_or_none(id=user_id)
    return _user


@router.post("/logout", summary="Выйти")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.delete("/{user_id}", summary="Удаляем пользователя с бд")
async def user_delete(db: DBDep, user_id: int):
    await db.users.delete(id=user_id)
    await db.commit()
    return {"status": "OK"}

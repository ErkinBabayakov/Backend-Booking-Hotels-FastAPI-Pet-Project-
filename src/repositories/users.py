from sqlalchemy import select
from pydantic import EmailStr

from sqlalchemy.exc import NoResultFound, IntegrityError
from src.exceptions import EmailNotRegisteredException, EmailNotCorrectException
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashPassword


class UserRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hash_password(self, email: EmailStr):
        try:
            query = select(self.model).filter_by(email=email)
            result = await self.session.execute(query)
            model = result.scalars().one()
        except NoResultFound as ex:
            raise EmailNotRegisteredException from ex
        except IntegrityError as ex:
            raise EmailNotCorrectException from ex
        return UserWithHashPassword.model_validate(model)

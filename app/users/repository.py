from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from users.models import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.scalars(query)
        return result.one_or_none()

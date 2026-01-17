from common.pagination import CustomPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import UserModel
from users.schemas.users import UserListResponseSchema


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_external_id(self, external_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == external_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_list(self) -> CustomPage[UserListResponseSchema]:
        users = select(UserModel)
        return await paginate(self.session, users)

    def add(self, user: UserModel) -> None:
        self.session.add(user)

    def update_from_api(self, user: UserModel, data: dict) -> None:
        user.name = data["name"]
        user.email = data["email"]
        user.username = data["username"]

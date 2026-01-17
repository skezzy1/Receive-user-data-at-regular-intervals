import logging
import httpx
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from core.config import get_settings
from users.repository import UserRepository

from users.models import UserModel

from users.schemas.users import UserListResponseSchema, CustomPage

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: AsyncSession, repo: UserRepository):
        self.db = db
        self.repo = repo
        self.API_URL: str = get_settings().API_URL

    async def _get_user_or_404(self, id: int) -> UserModel:
        user = await self.repo.get_user_by_id(UserModel.id == id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_user_list_from_api(self) -> CustomPage[UserListResponseSchema]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.API_URL)
            response.raise_for_status()
            data = response.json()
            return data

    async def get_user_by_id(self, id: int) -> UserModel | None:
        return await self._get_user_or_404(id)

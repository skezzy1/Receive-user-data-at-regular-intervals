import httpx
from common.messages import USER_NOT_FOUND
from common.pagination import CustomPage
from core.config import get_settings
from fastapi import HTTPException
from users.models import UserModel
from users.repository import UserRepository
from users.schemas.users import UserListResponseSchema


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.api_url = get_settings().API_USERS

    async def get_user_or_404(self, user_id: int) -> UserModel:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
        return user

    async def fetch_users_from_api(self) -> list[UserModel]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.api_url)
            response.raise_for_status()
            return response.json()

    async def get_user_list(
            self, payload: UserListResponseSchema
    ) -> CustomPage[UserListResponseSchema]:
        return await self.repo.get_user_list(payload)

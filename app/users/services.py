import requests
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

    def get_user_or_404(self, user_id: int) -> UserModel:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
        return user

    def fetch_users_from_api(self) -> list[dict]:
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=503, detail=f"External API error: {e}")

    def get_user_list(self) -> CustomPage[UserListResponseSchema]:
        return self.repo.get_user_list()

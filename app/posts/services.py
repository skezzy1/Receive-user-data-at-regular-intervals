import httpx
from common.messages import POST_NOT_FOUND
from core.config import get_settings
from fastapi import HTTPException
from posts.models import PostModel
from posts.repository import PostsRepository
from posts.schemas import PostListResponseSchema
from common.pagination import CustomPage


class PostsService:
    def __init__(self, repo: PostsRepository):
        self.repo = repo
        self.api_url = get_settings().API_POSTS

    async def get_post_or_404(self, id: int) -> PostModel:
        post = await self.repo.get_post_by_id(id)
        if post is None:
            raise HTTPException(status_code=404, detail=POST_NOT_FOUND)
        return post

    async def get_posts_list(
            self, payload: PostListResponseSchema
    ) -> CustomPage[PostListResponseSchema]:
        return await self.repo.get_user_list(payload)

    async def fetch_posts_from_api(self) -> list[PostModel]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.api_url)
            response.raise_for_status()
            return response.json()

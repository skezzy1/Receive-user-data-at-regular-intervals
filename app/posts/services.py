import requests
from fastapi import HTTPException
from common.messages import POST_NOT_FOUND
from core.config import get_settings
from posts.models import PostModel
from posts.repository import PostsRepository
from posts.schemas import PostListResponseSchema
from common.pagination import CustomPage


class PostsService:
    def __init__(self, repo: PostsRepository):
        self.repo = repo
        self.api_url = get_settings().API_POSTS

    def get_post_or_404(self, id: int) -> PostModel:
        post = self.repo.get_post_by_id(id)
        if post is None:
            raise HTTPException(status_code=404, detail=POST_NOT_FOUND)
        return post

    def get_posts_list(self) -> CustomPage[PostListResponseSchema]:
        return self.repo.get_posts_list()

    def fetch_posts_from_api(self) -> list[dict]:
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=503, detail=f"External API error: {e}")

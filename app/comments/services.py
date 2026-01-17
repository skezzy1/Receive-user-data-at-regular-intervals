import httpx
from common.messages import COMMENT_NOT_FOUND
from core.config import get_settings
from fastapi import HTTPException
from comments.models import CommentsModel
from comments.repository import CommentsRepository


class CommentsService:
    def __init__(self, repo: CommentsRepository):
        self.repo = repo
        self.api_url = get_settings().API_COMMENTS

    async def get_comments_or_404(self, id: int) -> CommentsModel:
        comment = await self.repo.get_comment_by_id(id)
        if comment is None:
            raise HTTPException(status_code=404, detail=COMMENT_NOT_FOUND)
        return comment

    async def fetch_comments_from_api(self) -> list[CommentsModel]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.api_url)
            response.raise_for_status()
            return response.json()

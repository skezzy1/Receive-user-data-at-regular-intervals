import requests
from fastapi import HTTPException
from common.messages import COMMENT_NOT_FOUND
from core.config import get_settings
from comments.models import CommentsModel
from comments.repository import CommentsRepository
from common.pagination import CustomPage
from comments.schemas import CommentsPostResponseListSchema


class CommentsService:
    def __init__(self, repo: CommentsRepository):
        self.repo = repo
        self.api_url = get_settings().API_COMMENTS

    def get_comments_or_404(self, id: int) -> CommentsModel:
        comment = self.repo.get_comment_by_id(id)
        if comment is None:
            raise HTTPException(status_code=404, detail=COMMENT_NOT_FOUND)
        return comment

    def get_comments_list(self) -> CustomPage[CommentsPostResponseListSchema]:
        return self.repo.get_comments_list()

    def fetch_comments_from_api(self) -> list[dict]:
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=503, detail=f"External API error: {e}")

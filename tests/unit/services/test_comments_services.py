import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy import select

from comments.models import CommentsModel
from comments.services import CommentsService
from comments.repository import CommentsRepository


class TestCommentsService:
    def test_get_comments_or_404_existing_comment(self, test_session, sample_comment):
        repo = CommentsRepository(test_session)
        service = CommentsService(repo)
        comment = service.get_comments_or_404(sample_comment.id)
        assert comment is not None

    def test_get_comments_or_404_non_existing_comment(self, test_session):
        repo = CommentsRepository(test_session)
        service = CommentsService(repo)
        with pytest.raises(HTTPException) as exc_info:
            service.get_comments_or_404(999)
        assert exc_info.value.status_code == 404

    def test_get_comments_list(self, test_session, sample_comment):
        repo = CommentsRepository(test_session)
        service = CommentsService(repo)

        query = select(CommentsModel)
        result = test_session.execute(query).scalars().all()
        assert len(result) > 0

    @patch('comments.services.requests.get')
    def test_fetch_comments_from_api_success(self, mock_get, test_session):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "Comment 1", "email": "test@example.com",
             "body": "Body", "postId": 1}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        repo = CommentsRepository(test_session)
        service = CommentsService(repo)
        comments = service.fetch_comments_from_api()
        assert len(comments) == 1

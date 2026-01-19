import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy import select

from posts.models import PostModel

from posts.services import PostsService
from posts.repository import PostsRepository


class TestPostsService:
    def test_get_post_or_404_existing_post(self, test_session, sample_post):
        repo = PostsRepository(test_session)
        service = PostsService(repo)
        post = service.get_post_or_404(sample_post.id)
        assert post is not None
        assert post.id == sample_post.id

    def test_get_post_or_404_non_existing_post(self, test_session):
        repo = PostsRepository(test_session)
        service = PostsService(repo)
        with pytest.raises(HTTPException) as exc_info:
            service.get_post_or_404(999)
        assert exc_info.value.status_code == 404

    def test_get_posts_list(self, test_session, sample_post):
        repo = PostsRepository(test_session)

        query = select(PostModel)
        result = test_session.execute(query).scalars().all()
        assert len(result) > 0

    @patch('posts.services.requests.get')
    def test_fetch_posts_from_api_success(self, mock_get, test_session):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "title": "Post 1", "body": "Body 1", "userId": 1}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        repo = PostsRepository(test_session)
        service = PostsService(repo)
        posts = service.fetch_posts_from_api()
        assert len(posts) == 1

import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy import select

from users.models import UserModel

from users.services import UserService
from users.repository import UserRepository


class TestUserService:
    def test_get_user_or_404_existing_user(self):
        repo = Mock()
        repo.get_by_id.return_value = Mock(
            id=1,
            name="John Doe"
        )
        service = UserService(repo)
        user = service.get_user_or_404(1)
        assert user.id == 1

    def test_get_user_or_404_non_existing_user(self, test_session):
        repo = UserRepository(test_session)
        service = UserService(repo)
        with pytest.raises(HTTPException) as exc_info:
            service.get_user_or_404(999)
        assert exc_info.value.status_code == 404

    def test_get_user_list(self, test_session, sample_user):
        repo = UserRepository(test_session)
        service = UserService(repo)

        query = select(UserModel)
        result = test_session.execute(query).scalars().all()
        assert len(result) > 0

    @patch('users.services.requests.get')
    def test_fetch_users_from_api_success(self, mock_get, test_session):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "User 1", "email": "user1@example.com"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        repo = UserRepository(test_session)
        service = UserService(repo)
        users = service.fetch_users_from_api()

        assert len(users) == 1
        assert users[0]["name"] == "User 1"

    @patch('users.services.requests.get')
    def test_fetch_users_from_api_failure(self, mock_get, test_session):
        import requests
        mock_get.side_effect = requests.RequestException("API Error")

        repo = UserRepository(test_session)
        service = UserService(repo)
        with pytest.raises(HTTPException) as exc_info:
            service.fetch_users_from_api()
        assert exc_info.value.status_code == 503

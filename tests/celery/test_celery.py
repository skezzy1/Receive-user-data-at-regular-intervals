import pytest
from unittest.mock import patch, Mock, MagicMock
from core.celery.tasks import fetch_users_task, fetch_posts_task, fetch_comments_task


class TestCeleryTasks:
    @patch('core.celery.tasks.get_postgresql_db_contextmanager')
    @patch('core.celery.tasks.UserImporter')
    def test_fetch_users_task_success(self, mock_importer_class, mock_db_context):
        mock_session = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_session

        mock_importer = Mock()
        mock_importer_class.return_value = mock_importer

        fetch_users_task()

        mock_importer_class.assert_called_once_with(mock_session)
        mock_importer.run.assert_called_once()

    @patch('core.celery.tasks.get_postgresql_db_contextmanager')
    @patch('core.celery.tasks.UserImporter')
    def test_fetch_users_task_error_handling(self, mock_importer_class, mock_db_context):
        mock_session = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_session

        mock_importer = Mock()
        mock_importer.run.side_effect = Exception("Import error")
        mock_importer_class.return_value = mock_importer

        with pytest.raises(Exception) as exc_info:
            fetch_users_task()

        assert str(exc_info.value) == "Import error"

    @patch('core.celery.tasks.get_postgresql_db_contextmanager')
    @patch('core.celery.tasks.PostImporter')
    def test_fetch_posts_task_success(self, mock_importer_class, mock_db_context):
        mock_session = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_session

        mock_importer = Mock()
        mock_importer_class.return_value = mock_importer

        fetch_posts_task()

        mock_importer_class.assert_called_once_with(mock_session)
        mock_importer.run.assert_called_once()

    @patch('core.celery.tasks.get_postgresql_db_contextmanager')
    @patch('core.celery.tasks.PostImporter')
    def test_fetch_posts_task_session_cleanup(self, mock_importer_class, mock_db_context):
        """Тест що сесія правильно закривається після виконання task"""
        mock_session = MagicMock()
        mock_context_manager = MagicMock()
        mock_context_manager.__enter__.return_value = mock_session
        mock_db_context.return_value = mock_context_manager

        mock_importer = Mock()
        mock_importer_class.return_value = mock_importer

        fetch_posts_task()

        mock_db_context.assert_called_once()
        mock_context_manager.__enter__.assert_called_once()
        mock_context_manager.__exit__.assert_called_once()

    @patch('core.celery.tasks.get_postgresql_db_contextmanager')
    @patch('core.celery.tasks.CommentImporter')
    def test_fetch_comments_task_success(self, mock_importer_class, mock_db_context):
        mock_session = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_session

        mock_importer = Mock()
        mock_importer_class.return_value = mock_importer

        fetch_comments_task()

        mock_importer_class.assert_called_once_with(mock_session)
        mock_importer.run.assert_called_once()


class TestCeleryConfiguration:
    def test_celery_app_configuration(self):
        from core.celery.client import celery_app

        assert celery_app.conf.task_serializer == "json"
        assert "json" in celery_app.conf.accept_content
        assert celery_app.conf.result_serializer == "json"
        assert celery_app.conf.timezone == "UTC"
        assert celery_app.conf.enable_utc is True

    def test_celery_beat_schedule_configuration(self):
        from core.celery.client import celery_app

        beat_schedule = celery_app.conf.beat_schedule

        assert "fetch-users" in beat_schedule
        assert "fetch-posts" in beat_schedule
        assert "fetch-comments" in beat_schedule

        assert beat_schedule["fetch-users"]["task"] == "core.celery.tasks.fetch_users_task"
        assert beat_schedule["fetch-posts"]["task"] == "core.celery.tasks.fetch_posts_task"
        assert beat_schedule["fetch-comments"]["task"] == "core.celery.tasks.fetch_comments_task"

    def test_celery_tasks_are_registered(self):
        from core.celery.client import celery_app

        registered_tasks = celery_app.tasks.keys()

        assert "core.celery.tasks.fetch_users_task" in registered_tasks
        assert "core.celery.tasks.fetch_posts_task" in registered_tasks
        assert "core.celery.tasks.fetch_comments_task" in registered_tasks


@pytest.mark.integration
class TestCeleryTasksIntegration:
    @patch('core.importer.client.requests.get')
    def test_fetch_users_task_integration(self, mock_get, test_session):
        from core.celery.tasks import fetch_users_task
        from users.models import UserModel

        mock_response = Mock()
        mock_response.json.return_value = [{
            "id": 1, "name": "Test User", "username": "testuser",
            "email": "test@example.com", "phone": "123",
            "website": "test.com",
            "address": {
                "street": "St", "suite": "1", "city": "City",
                "zipcode": "00000",
                "geo": {"lat": "50.0", "lng": "30.0"}
            },
            "company": {
                "name": "Company", "catchPhrase": "Phrase", "bs": "bs"
            }
        }]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch('core.celery.tasks.get_postgresql_db_contextmanager') as mock_ctx:
            mock_ctx.return_value.__enter__.return_value = test_session

            fetch_users_task()

        users = test_session.query(UserModel).all()
        assert len(users) == 1
        assert users[0].name == "Test User"

    @patch('core.importer.client.requests.get')
    def test_full_celery_workflow_integration(self, mock_get, test_session):
        from core.celery.tasks import fetch_users_task, fetch_posts_task, fetch_comments_task
        from users.models import UserModel
        from posts.models import PostModel
        from comments.models import CommentsModel

        def get_side_effect(url):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None

            if "users" in url:
                mock_response.json.return_value = [{
                    "id": 1, "name": "User", "username": "user",
                    "email": "user@test.com", "phone": "123",
                    "website": "test.com",
                    "address": {
                        "street": "St", "suite": "1", "city": "City",
                        "zipcode": "00000",
                        "geo": {"lat": "50.0", "lng": "30.0"}
                    },
                    "company": {"name": "Co", "catchPhrase": "", "bs": ""}
                }]
            elif "posts" in url:
                mock_response.json.return_value = [{
                    "id": 1, "title": "Post", "body": "Body", "userId": 1
                }]
            elif "comments" in url:
                mock_response.json.return_value = [{
                    "id": 1, "name": "Comment", "email": "c@test.com",
                    "body": "Body", "postId": 1
                }]

            return mock_response

        mock_get.side_effect = get_side_effect

        with patch('core.celery.tasks.get_postgresql_db_contextmanager') as mock_ctx:
            mock_ctx.return_value.__enter__.return_value = test_session

            fetch_users_task()
            fetch_posts_task()
            fetch_comments_task()

        assert test_session.query(UserModel).count() == 1
        assert test_session.query(PostModel).count() == 1
        assert test_session.query(CommentsModel).count() == 1

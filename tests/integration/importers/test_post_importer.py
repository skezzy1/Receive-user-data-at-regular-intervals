from unittest.mock import Mock, patch
from core.importer.client import UserImporter, PostImporter, CommentImporter
from posts.models import PostModel


class TestPostImporter:
    @patch('core.importer.client.requests.get')
    def test_post_importer_run_success(self, mock_get, test_session, sample_user):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "title": "Test Post",
                "body": "Test body",
                "userId": sample_user.id
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        importer = PostImporter(test_session)
        importer.run()

        post = test_session.query(PostModel).filter_by(id=1).first()
        assert post is not None
        assert post.title == "Test Post"
        assert post.user_id == sample_user.id

    @patch('core.importer.client.requests.get')
    def test_post_importer_skip_invalid_user(self, mock_get, test_session):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "title": "Test Post",
                "body": "Test body",
                "userId": 999
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        importer = PostImporter(test_session)
        importer.run()

        post = test_session.query(PostModel).filter_by(id=1).first()
        assert post is None

    def test_get_valid_user_ids(self, test_session, sample_user):
        importer = PostImporter(test_session)

        valid_ids = importer._get_valid_user_ids()

        assert sample_user.id in valid_ids

from unittest.mock import Mock, patch
from core.importer.client import UserImporter, PostImporter, CommentImporter
from comments.models import CommentsModel


class TestCommentImporter:
    @patch('core.importer.client.requests.get')
    def test_comment_importer_run_success(self, mock_get, test_session, sample_post):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "name": "Test Comment",
                "email": "test@example.com",
                "body": "Test body",
                "postId": sample_post.id
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        importer = CommentImporter(test_session)
        importer.run()

        comment = test_session.query(CommentsModel).filter_by(id=1).first()
        assert comment is not None
        assert comment.name == "Test Comment"
        assert comment.post_id == sample_post.id

    @patch('core.importer.client.requests.get')
    def test_comment_importer_skip_invalid_post(self, mock_get, test_session):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "name": "Test Comment",
                "email": "test@example.com",
                "body": "Test body",
                "postId": 999
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        importer = CommentImporter(test_session)
        importer.run()

        comment = test_session.query(CommentsModel).filter_by(id=1).first()
        assert comment is None

    def test_get_valid_post_ids(self, test_session, sample_post):
        importer = CommentImporter(test_session)

        valid_ids = importer._get_valid_post_ids()

        assert sample_post.id in valid_ids

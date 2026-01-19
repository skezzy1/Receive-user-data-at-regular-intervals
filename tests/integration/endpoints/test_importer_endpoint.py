from unittest.mock import patch, Mock
from db.base_model import BaseModel
from main import app


class TestImportersIntegration:
    @patch('core.importer.client.requests.get')
    def test_full_import_workflow(self, mock_get, integration_session):
        from core.importer.client import UserImporter, PostImporter, CommentImporter

        def get_side_effect(url, *args, **kwargs):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None

            if "users" in url:
                mock_response.json.return_value = [{
                    "id": 1, "name": "User 1", "username": "user1",
                    "email": "user1@test.com", "phone": "123",
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
            elif "posts" in url:
                mock_response.json.return_value = [{
                    "id": 1, "title": "Post 1", "body": "Body 1", "userId": 1
                }]
            elif "comments" in url:
                mock_response.json.return_value = [{
                    "id": 1, "name": "Comment 1", "email": "c@test.com",
                    "body": "Comment body", "postId": 1
                }]

            return mock_response

        mock_get.side_effect = get_side_effect

        user_importer = UserImporter(integration_session)
        user_importer.run()

        post_importer = PostImporter(integration_session)
        post_importer.run()

        comment_importer = CommentImporter(integration_session)
        comment_importer.run()

        from users.models import UserModel
        from posts.models import PostModel
        from comments.models import CommentsModel

        users = integration_session.query(UserModel).all()
        assert len(users) == 1

        posts = integration_session.query(PostModel).all()
        assert len(posts) == 1

        comments = integration_session.query(CommentsModel).all()
        assert len(comments) == 1

        assert posts[0].user_id == users[0].id
        assert comments[0].post_id == posts[0].id

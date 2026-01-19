from comments.repository import CommentsRepository
from comments.models import CommentsModel


class TestCommentsRepository:
    def test_get_comment_by_id_existing(self, test_session, sample_comment):
        repo = CommentsRepository(test_session)
        comment = repo.get_comment_by_id(sample_comment.id)

        assert comment is not None
        assert comment.id == sample_comment.id
        assert comment.name == "Test Comment"
        assert comment.email == "test@example.com"

    def test_get_comment_by_id_non_existing(self, test_session):
        repo = CommentsRepository(test_session)
        comment = repo.get_comment_by_id(999)

        assert comment is None

    def test_get_comments_list(self, test_session, sample_comment):
        from sqlalchemy import select

        query = select(CommentsModel)
        result = test_session.execute(query).scalars().all()

        assert len(result) > 0
        assert result[0].id == sample_comment.id

    def test_get_comments_list_multiple(self, test_session, sample_post):
        from sqlalchemy import select

        for i in range(5):
            comment = CommentsModel(
                id=i + 10,
                name=f"Comment {i}",
                email=f"user{i}@example.com",
                body=f"Comment body {i}",
                post_id=sample_post.id
            )
            test_session.add(comment)
        test_session.commit()

        query = select(CommentsModel)
        result = test_session.execute(query).scalars().all()

        assert len(result) >= 5

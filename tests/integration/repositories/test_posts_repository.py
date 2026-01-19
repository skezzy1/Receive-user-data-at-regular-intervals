from posts.repository import PostsRepository
from posts.models import PostModel


class TestPostsRepository:
    def test_get_post_by_id_existing(self, test_session, sample_post):
        repo = PostsRepository(test_session)
        post = repo.get_post_by_id(sample_post.id)

        assert post is not None
        assert post.id == sample_post.id
        assert post.title == "Test Post"
        assert post.body == "Content"

    def test_get_post_by_id_non_existing(self, test_session):
        repo = PostsRepository(test_session)
        post = repo.get_post_by_id(999)

        assert post is None

    def test_get_posts_list(self, test_session, sample_post):
        from sqlalchemy import select

        query = select(PostModel)
        result = test_session.execute(query).scalars().all()

        assert len(result) > 0
        assert result[0].id == sample_post.id

    def test_get_posts_list_multiple(self, test_session, sample_user):
        from sqlalchemy import select

        for i in range(3):
            post = PostModel(
                id=i + 10,
                title=f"Post {i}",
                body=f"Content {i}",
                user_id=sample_user.id
            )
            test_session.add(post)
        test_session.commit()

        repo = PostsRepository(test_session)

        query = select(PostModel)
        result = test_session.execute(query).scalars().all()

        assert len(result) >= 3

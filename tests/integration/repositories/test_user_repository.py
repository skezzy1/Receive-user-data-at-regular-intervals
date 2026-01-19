from users.repository import UserRepository
from users.models import UserModel


class TestUserRepository:
    def test_get_by_id_existing_user(self, test_session, sample_user):
        repo = UserRepository(test_session)
        user = repo.get_by_id(sample_user.id)

        assert user is not None
        assert user.id == sample_user.id
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    def test_get_by_id_non_existing_user(self, test_session):
        repo = UserRepository(test_session)
        user = repo.get_by_id(999)

        assert user is None

    def test_get_user_list(self, test_session, sample_user):
        from sqlalchemy import select

        query = select(UserModel)
        result = test_session.execute(query).scalars().all()

        assert len(result) > 0
        assert result[0].id == sample_user.id

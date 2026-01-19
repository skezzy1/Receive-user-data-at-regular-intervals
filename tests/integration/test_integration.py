from db.base_model import BaseModel
from main import app


class TestDatabaseIntegration:
    def test_cascade_relationships(self, integration_session):
        from users.models import UserModel, AddressModel, GeoModel
        from company.models import CompanyModel
        from posts.models import PostModel
        from comments.models import CommentsModel

        geo = GeoModel(lat=50.0, lng=30.0)
        integration_session.add(geo)
        integration_session.flush()

        address = AddressModel(
            street="St", suite="1", city="City",
            zipcode="00000", geo=geo
        )
        integration_session.add(address)
        integration_session.flush()

        company = CompanyModel(name="Co", catchPhrase="", bs="")
        integration_session.add(company)
        integration_session.flush()

        user = UserModel(
            id=1, name="User", username="user",
            email="user@test.com", password="pass",
            phone="123", website="site.com",
            address=address, company=company
        )
        integration_session.add(user)
        integration_session.flush()

        post = PostModel(id=1, title="Post", body="Body", user_id=1)
        integration_session.add(post)
        integration_session.flush()

        comment = CommentsModel(
            id=1, name="Comment", email="c@test.com",
            body="Body", post_id=1
        )
        integration_session.add(comment)
        integration_session.commit()

        loaded_user = integration_session.query(UserModel).first()
        assert loaded_user.address is not None
        assert loaded_user.company is not None

        loaded_post = integration_session.query(PostModel).first()
        assert loaded_post.user_id == loaded_user.id

        loaded_comment = integration_session.query(CommentsModel).first()
        assert loaded_comment.post_id == loaded_post.id

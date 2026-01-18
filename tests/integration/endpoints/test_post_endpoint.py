from db.base_model import BaseModel
from main import app
from tests.conftest import API_PREFIX


class TestPostEndpointsIntegration:
    def test_get_posts_empty_list(self, client):
        response = client.get(f"{API_PREFIX}/posts/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 0

    def test_get_post_not_found(self, client):
        response = client.get(f"{API_PREFIX}/posts/999")
        assert response.status_code == 404

    def test_full_post_workflow(self, client, integration_session):
        from users.models import UserModel, AddressModel, GeoModel
        from company.models import CompanyModel
        from posts.models import PostModel

        geo = GeoModel(lat=50.0, lng=30.0)
        integration_session.add(geo)
        integration_session.flush()

        address = AddressModel(street="St", suite="1", city="City", zipcode="00000", geo=geo)
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

        post = PostModel(id=1, title="Test Post", body="Test content", user_id=1)
        integration_session.add(post)
        integration_session.commit()

        response = client.get(f"{API_PREFIX}/posts/")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1

        response = client.get(f"{API_PREFIX}/posts/1")
        assert response.status_code == 200
        assert response.json()["title"] == "Test Post"

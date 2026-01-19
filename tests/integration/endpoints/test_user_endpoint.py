from db.base_model import BaseModel
from main import app
from tests.conftest import API_PREFIX


class TestUserEndpointsIntegration:
    def test_get_users_empty_list(self, client):
        response = client.get(f"{API_PREFIX}/users/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 0

    def test_get_user_not_found(self, client):
        response = client.get(f"{API_PREFIX}/users/999")
        assert response.status_code == 404

    def test_full_user_workflow(self, client, integration_session):
        from users.models import UserModel, AddressModel, GeoModel
        from company.models import CompanyModel

        geo = GeoModel(lat=50.4501, lng=30.5234)
        integration_session.add(geo)
        integration_session.flush()

        address = AddressModel(street="Test St", suite="1", city="Kyiv", zipcode="01001", geo=geo)
        integration_session.add(address)
        integration_session.flush()

        company = CompanyModel(name="Test Co", catchPhrase="Test", bs="test")
        integration_session.add(company)
        integration_session.flush()

        user = UserModel(
            id=1, name="Test User", username="testuser",
            email="test@example.com", password="pass",
            phone="123", website="test.com",
            address=address, company=company
        )
        integration_session.add(user)
        integration_session.commit()

        response = client.get(f"{API_PREFIX}/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1

        response = client.get(f"{API_PREFIX}/users/1")
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["name"] == "Test User"

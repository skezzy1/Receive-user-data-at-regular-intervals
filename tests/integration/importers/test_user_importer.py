import pytest
from unittest.mock import Mock, patch
from core.importer.client import UserImporter, PostImporter, CommentImporter
from users.models import UserModel, GeoModel, AddressModel


class TestUserImporter:
    @patch('core.importer.client.requests.get')
    def test_user_importer_run_success(self, mock_get, test_session):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "name": "Test User",
                "username": "testuser",
                "email": "test@example.com",
                "phone": "123-456-7890",
                "website": "test.com",
                "address": {
                    "street": "Main St",
                    "suite": "Apt 1",
                    "city": "Kyiv",
                    "zipcode": "01001",
                    "geo": {"lat": "50.4501", "lng": "30.5234"}
                },
                "company": {
                    "name": "Test Company",
                    "catchPhrase": "Test phrase",
                    "bs": "test bs"
                }
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        importer = UserImporter(test_session)
        importer.run()

        user = test_session.query(UserModel).filter_by(id=1).first()
        assert user is not None
        assert user.name == "Test User"
        assert user.email == "test@example.com"

        assert user.address is not None
        assert user.company is not None
        assert user.address.geo is not None

    def test_get_or_create_geo_new(self, test_session):
        importer = UserImporter(test_session)

        geo = importer._get_or_create_geo(50.4501, 30.5234)

        assert geo is not None
        assert geo.lat == 50.4501
        assert geo.lng == 30.5234

    def test_get_or_create_geo_existing(self, test_session, sample_geo):
        importer = UserImporter(test_session)

        geo = importer._get_or_create_geo(sample_geo.lat, sample_geo.lng)

        assert geo.id == sample_geo.id

    def test_get_or_create_address_new(self, test_session, sample_geo):
        importer = UserImporter(test_session)

        address_data = {
            "street": "New Street",
            "suite": "Suite 1",
            "city": "Kyiv",
            "zipcode": "02002"
        }

        address = importer._get_or_create_address(address_data, sample_geo)

        assert address is not None
        assert address.zipcode == "02002"
        assert address.geo == sample_geo

    def test_get_or_create_company_new(self, test_session):
        importer = UserImporter(test_session)

        company_data = {
            "name": "New Company",
            "catchPhrase": "New phrase",
            "bs": "new bs"
        }

        company = importer._get_or_create_company(company_data)

        assert company is not None
        assert company.name == "New Company"

    @patch('core.importer.client.requests.get')
    def test_user_importer_api_error(self, mock_get, test_session):
        mock_get.side_effect = Exception("API Error")

        importer = UserImporter(test_session)

        with pytest.raises(Exception):
            importer.run()

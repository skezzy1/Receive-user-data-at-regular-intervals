import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from db.base_model import BaseModel
from users.models import UserModel, AddressModel, CompanyModel, GeoModel
from posts.models import PostModel
from comments.models import CommentsModel
from main import app

API_PREFIX = "/api/v1"


@pytest.fixture(scope="function")
def integration_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    BaseModel.metadata.create_all(bind=engine)
    yield engine
    BaseModel.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def integration_session(integration_engine):
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=integration_engine
    )
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(integration_session):
    def override_get_db():
        try:
            yield integration_session
        finally:
            pass

    try:
        from db.session_postgresql import get_postgresql_db as get_db_func
    except ImportError:
        from db.session import get_postgresql_db as get_db_func

    app.dependency_overrides[get_db_func] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture(scope="session")
def tables(engine):
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def sample_geo(test_session):
    geo = GeoModel(
        id=1,
        lat="-37.3159",
        lng="81.1496"
    )
    test_session.add(geo)
    test_session.commit()
    return geo


@pytest.fixture
def sample_address(test_session, sample_geo):
    address = AddressModel(
        id=1,
        street="Kulas Light",
        suite="Apt. 556",
        city="Gwenborough",
        zipcode="92998-3874",
        geo_id=sample_geo.id
    )
    test_session.add(address)
    test_session.commit()
    return address


@pytest.fixture
def sample_company(test_session):
    company = CompanyModel(
        id=1,
        name="Romaguera-Crona",
        catchPhrase="Multi-layered client-server neural-net",
        bs="harness real-time e-markets"
    )
    test_session.add(company)
    test_session.commit()
    return company


@pytest.fixture
def sample_user(test_session, sample_address, sample_company):
    user = UserModel(
        id=1,
        name="John Doe",
        username="johndoe",
        email="john@example.com",
        password="securepassword",
        phone="1-770-736-8031 x56442",
        website="hildegard.org",
        address_id=sample_address.id,
        company_id=sample_company.id
    )
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def sample_post(test_session, sample_user):
    post = PostModel(
        id=1,
        title="Test Post",
        body="Content",
        user_id=sample_user.id
    )
    test_session.add(post)
    test_session.commit()
    return post


@pytest.fixture
def sample_comment(test_session, sample_post):
    comment = CommentsModel(
        id=1,
        name="Test Comment",
        body="Comment Body",
        email="test@example.com",
        post_id=sample_post.id
    )
    test_session.add(comment)
    test_session.commit()
    return comment

import logging
from typing import Optional, ClassVar

from pydantic import EmailStr

from core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True
    title: str = 'Test FastAPI Application'

    SECRET_KEY: str = 'test_secret_key_for_jwt_generation_592833c3e19d66be3'

    logging_level: int = logging.DEBUG

    EMAIL_USERNAME: str = 'test_user'
    EMAIL_PASSWORD: str = 'test_password'
    EMAIL_FROM: EmailStr = 'no-reply@test.com'
    EMAIL_PORT: int = 587
    EMAIL_SERVER: str = 'smtp.test.com'
    EMAIL_FROM_NAME: str = 'Test System'
    EMAIL_HOST: str = 'test'

    DATABASE_NAME: str = 'test_db'

    TESTING: bool = True
    ENVIRONMENT: str = "test"

    SENTRY_DSN: Optional[str] = None

    AWS_ACCESS_KEY_ID: str = "testing"
    AWS_SECRET_ACCESS_KEY: str = "testing"
    AWS_STORAGE_BUCKET_NAME: str = "test-bucket"
    AWS_REGION: str = "us-east-1"

    INVITE_EXPIRATION_MINUTES: ClassVar[int] = 10

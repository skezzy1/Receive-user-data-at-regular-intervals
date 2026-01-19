import os
from typing import ClassVar

from core.settings.app import AppSettings


class QAAppSettings(AppSettings):
    MAIL_STARTTLS: bool = True

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    SENTRY_DSN: str | None = os.getenv('SENTRY_DSN')

    INVITE_EXPIRATION_MINUTES: ClassVar[int] = 10

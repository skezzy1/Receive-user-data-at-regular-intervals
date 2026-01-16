import logging
import os
from typing import ClassVar

from app.core.settings.app import AppSettings


class ProductionAppSettings(AppSettings):
    MAIL_STARTTLS: bool = True
    logging_level: int = logging.INFO

    SENTRY_DSN: str | None = os.getenv('SENTRY_DSN')

    INVITE_EXPIRATION_MINUTES: ClassVar[int] = 60 * 24 * 3

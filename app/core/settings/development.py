import logging

from dotenv import load_dotenv

from core.settings.app import AppSettings

load_dotenv()


class DevelopmentAppSettings(AppSettings):
    debug: bool = True

    title: str = 'Development FastAPI example application'

    logging_level: int = logging.DEBUG

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1500 * 60

    SMTP_TIMEOUT: int = 10

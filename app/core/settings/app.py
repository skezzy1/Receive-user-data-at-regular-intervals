import os
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy import URL

load_dotenv()


class AppSettings(BaseSettings):
    SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")

    DATABASE_USER: str = os.getenv("POSTGRES_USER")
    DATABASE_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DATABASE_HOST: str = os.getenv("POSTGRES_HOST")
    DATABASE_PORT: int = os.getenv("POSTGRES_PORT")
    DATABASE_NAME: str = os.getenv("POSTGRES_DB")
    DATABASE_URI: URL = URL.create(
        drivername="postgresql+psycopg",
        username=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME,
    )

    TESTING: bool = 0

    DOMAINS: set[str] = set()

    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent
    DATABASE_DIR: ClassVar[Path] = BASE_DIR / "db"
    API_BASE_URL: str = os.getenv("API_BASE_URL")
    API_USERS: str = os.getenv("API_USERS")
    API_POSTS: str = os.getenv("API_POSTS")
    API_COMMENTS: str = os.getenv("API_COMMENTS")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")

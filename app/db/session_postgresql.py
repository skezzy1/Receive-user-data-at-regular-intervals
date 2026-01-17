import os
import ssl
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from urllib.parse import quote_plus

from core.config import get_settings
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv(verbose=True)

settings = get_settings()

USER = quote_plus(settings.DATABASE_USER)
PASSWORD = settings.DATABASE_PASSWORD
HOST = settings.DATABASE_HOST
PORT = settings.DATABASE_PORT
DB_NAME = settings.DATABASE_NAME
DRIVER = "postgresql+asyncpg"
ENVIRONMENT = os.getenv("ENVIRONMENT")


def get_ssl_context() -> Optional[ssl.SSLContext]:
    if ENVIRONMENT == "development":
        return None

    try:
        cert_path = settings.SECRET_KEYS_DIR / "aws_secret_key.pem"

        if not cert_path.exists():
            print(f"Warning: SSL certificate not found at {cert_path}")
            return None

        ssl_context = ssl.create_default_context(cafile=str(cert_path))
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        return ssl_context

    except Exception as e:
        print(f"Warning: Failed to create SSL context: {e}")
        return None


ssl_ctx = get_ssl_context()
connect_args = {"ssl": ssl_ctx} if ssl_ctx else {}

POSTGRESQL_DATABASE_URL = f"{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

postgresql_engine = create_async_engine(
    POSTGRESQL_DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    bind=postgresql_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_postgresql_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_postgresql_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session using a context manager.
    """
    async with AsyncSessionLocal() as session:
        yield session

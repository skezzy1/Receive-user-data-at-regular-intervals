import os
import ssl
from contextlib import contextmanager
from typing import Generator, Optional
from urllib.parse import quote_plus

from core.config import get_settings
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class PostgresDatabase:
    def __init__(self):
        load_dotenv(verbose=True)
        self.settings = get_settings()

        self.environment = os.getenv("ENVIRONMENT")

        self.user = quote_plus(self.settings.DATABASE_USER)
        self.password = self.settings.DATABASE_PASSWORD
        self.host = self.settings.DATABASE_HOST
        self.port = self.settings.DATABASE_PORT
        self.db_name = self.settings.DATABASE_NAME

        self.driver = "postgresql"

        self.database_url = f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

        self.ssl_ctx = self._get_ssl_context()
        self.connect_args = {"ssl": self.ssl_ctx} if self.ssl_ctx else {}

        self.engine = create_engine(
            self.database_url,
            echo=False,
            connect_args=self.connect_args,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
        )

    def _get_ssl_context(self) -> Optional[ssl.SSLContext]:
        if self.environment == "development":
            return None

        try:
            cert_path = self.settings.SECRET_KEYS_DIR / "aws_secret_key.pem"

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

    def get_postgresql_db(self) -> Generator[Session, None, None]:
        """
        Provide a synchronous database session.
        """
        session = self.session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def get_postgresql_db_contextmanager(self) -> Generator[Session, None, None]:
        """
        Provide a synchronous database session using a context manager.
        """
        session = self.session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


db_manager = PostgresDatabase()

get_postgresql_db = db_manager.get_postgresql_db
get_postgresql_db_contextmanager = db_manager.get_postgresql_db_contextmanager
postgresql_engine = db_manager.engine

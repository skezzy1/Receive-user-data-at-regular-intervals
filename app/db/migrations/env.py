from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, engine_from_config

from db.base_model import BaseModel
from db.session_postgresql import postgresql_engine

import users.models  # type: ignore
import company.models  # type: ignore
import posts.models  # type: ignore
import comments.models  # type: ignore

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = postgresql_engine.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (SYNCHRONOUS)."""

    connectable = postgresql_engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

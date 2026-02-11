from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config

fileConfig(config.config_file_name)

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.models import SQLModel
from src.app.db import engine

target_metadata = SQLModel.metadata


def run_migrations_offline():
    context.configure(url=str(engine.url), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

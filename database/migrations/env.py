# database/migrations/env.py
import os
import sys
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Load .env so DATABASE_URL is available ──────────────────────────────────
# Walk up from migrations/ → database/ → project root
load_dotenv(
    os.path.join(os.path.dirname(__file__), '..', '..', '.env')
)

# ── Add project root to sys.path so imports work ────────────────────────────
# migrations/ is inside database/, database/ is inside project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# ── Import your models so Alembic can detect table changes ──────────────────
from database.models import Base          # ← THIS IS THE KEY LINE
target_metadata = Base.metadata           # ← Alembic reads this to find tables

# ── Alembic config setup ─────────────────────────────────────────────────────
config = context.config

# Inject the database URL from .env into alembic config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Used when you want to generate SQL without connecting to DB."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Normal mode — connects to DB and runs migrations live."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
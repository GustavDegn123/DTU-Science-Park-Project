from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine
from database.database import engine
from models.base import Base  # ← Importér kun Base!

# Importér modellerne, så Alembic ved, de findes
import models.startup
import models.investment

# Hent Alembic Config
config = context.config

# Opsæt logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata fra alle modeller
target_metadata = Base.metadata

async def run_migrations_online() -> None:
    """Kør migrationer i 'online' mode med AsyncEngine."""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection: Connection) -> None:
    """Konfigurer Alembic kontekst og kør migrationer."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True
    )
    
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_offline() -> None:
    """Kør migrationer i 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())

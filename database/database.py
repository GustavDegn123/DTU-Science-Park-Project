from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL  

# Opret den asynkrone database engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session factory
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency til FastAPI routes
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

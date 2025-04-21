from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.startup import Startup
from schemas.startup import StartupCreate, StartupResponse
from services.external_api import fetch_external_data
import pandas as pd

# ✅ Opret en ny startup
async def create_startup(db: AsyncSession, startup_data: StartupCreate) -> Startup:
    db_startup = Startup(**startup_data.dict())
    db.add(db_startup)
    await db.commit()
    await db.refresh(db_startup)
    return db_startup

# ✅ Hent alle startups
async def get_startups(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Startup).offset(skip).limit(limit))
    return result.scalars().all()

# ✅ Hent en startup via ID
async def get_startup_by_id(db: AsyncSession, startup_id: int):
    result = await db.execute(select(Startup).where(Startup.id == startup_id))
    return result.scalars().first()

# ✅ Opdater en startup
async def update_startup(db: AsyncSession, startup_id: int, startup_update: StartupCreate):
    startup = await get_startup_by_id(db, startup_id)
    if not startup:
        return None
    
    for key, value in startup_update.dict(exclude_unset=True).items():
        setattr(startup, key, value)

    await db.commit()
    await db.refresh(startup)
    return startup

# ✅ Slet en startup
async def delete_startup(db: AsyncSession, startup_id: int):
    startup = await get_startup_by_id(db, startup_id)
    if not startup:
        return None
    
    await db.delete(startup)
    await db.commit()
    return startup

async def update_impact_scores(db: AsyncSession):
    """
    Opdaterer impact scores i databasen for alle startups.
    """
    result = await db.execute(select(Startup))
    startups = result.scalars().all()

    if not startups:
        return {"message": "No startups found"}

    for s in startups:
        # Hent eksterne data (f.eks. ESG-score fra API)
        external_data = fetch_external_data()

        # Opdater startup med de nye værdier
        s.esg_score = external_data["esg_score"]
        s.traction = external_data["traction"]
        s.sdg_alignment = external_data["sdg_alignment"]

        # Impact Score beregning
        s.impact_score = (
            s.esg_score * 0.30 +
            s.traction * 0.25 +
            70 * 0.20 +  # Team score (midlertidig hardcoded)
            (s.funding_history or 0) * 0.15 +
            s.sdg_alignment * 0.10
        )

    await db.commit()  # Gem alle ændringer i databasen
    return {"message": "Impact scores updated successfully"}


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.matchmaking import Matchmaking
from schemas.matchmaking import MatchmakingCreate

# ✅ Opret en ny matchmaking
async def create_matchmaking(db: AsyncSession, matchmaking_data: MatchmakingCreate) -> Matchmaking:
    db_matchmaking = Matchmaking(**matchmaking_data.dict())
    db_matchmaking.status = "Accepted"  # 🎯 Tvinger status til "Accepted"
    db.add(db_matchmaking)
    await db.commit()
    await db.refresh(db_matchmaking)
    return db_matchmaking

# ✅ Hent alle matchmakings
async def get_matchmakings(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Matchmaking).offset(skip).limit(limit))
    return result.scalars().all()

# ✅ Hent en matchmaking via ID
async def get_matchmaking_by_id(db: AsyncSession, matchmaking_id: int):
    result = await db.execute(select(Matchmaking).where(Matchmaking.id == matchmaking_id))
    return result.scalars().first()

# ✅ Slet en matchmaking
async def delete_matchmaking(db: AsyncSession, matchmaking_id: int):
    matchmaking = await get_matchmaking_by_id(db, matchmaking_id)
    if not matchmaking:
        return None
    
    await db.delete(matchmaking)
    await db.commit()
    return matchmaking

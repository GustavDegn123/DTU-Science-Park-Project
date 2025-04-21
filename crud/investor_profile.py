from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.investor_profile import InvestorProfile
from schemas.investor_profile import InvestorProfileCreate, InvestorProfileResponse

# ✅ Opret en ny investor-profil
async def create_investor_profile(db: AsyncSession, profile_data: InvestorProfileCreate) -> InvestorProfile:
    db_profile = InvestorProfile(**profile_data.dict())
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile

# ✅ Hent en investor-profil via investor_id
async def get_investor_profile_by_investor_id(db: AsyncSession, investor_id: int):
    result = await db.execute(select(InvestorProfile).where(InvestorProfile.investor_id == investor_id))
    return result.scalars().first()

# ✅ Opdater en investor-profil
async def update_investor_profile(db: AsyncSession, investor_id: int, profile_update: InvestorProfileCreate):
    profile = await get_investor_profile_by_investor_id(db, investor_id)
    if not profile:
        return None
    
    for key, value in profile_update.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return profile

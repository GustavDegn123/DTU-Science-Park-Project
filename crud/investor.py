from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.investor import Investor
from schemas.investor import InvestorCreate, InvestorResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Opret en ny investor
async def create_investor(db: AsyncSession, investor_data: InvestorCreate) -> Investor:
    existing_investor = await db.execute(select(Investor).filter(Investor.email == investor_data.email))
    if existing_investor.scalars().first():
        raise ValueError(f"Investor med e-mail {investor_data.email} findes allerede!")

    hashed_pw = pwd_context.hash(investor_data.password)
    db_investor = Investor(**investor_data.dict(exclude={"password"}))
    db_investor.password = hashed_pw

    db.add(db_investor)
    await db.commit()
    await db.refresh(db_investor)
    return db_investor

# ✅ Hent alle investorer
async def get_investors(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Investor).offset(skip).limit(limit))
    return result.scalars().all()

# ✅ Hent en investor via ID
async def get_investor_by_id(db: AsyncSession, investor_id: int):
    result = await db.execute(select(Investor).where(Investor.id == investor_id))
    return result.scalars().first()

# ✅ Hent en investor baseret på email
async def get_investor_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Investor).where(Investor.email == email))
    return result.scalars().first()

# ✅ Opdater en investor
async def update_investor(db: AsyncSession, investor_id: int, investor_update: InvestorCreate):
    investor = await get_investor_by_id(db, investor_id)
    if not investor:
        return None
    
    for key, value in investor_update.dict(exclude_unset=True).items():
        setattr(investor, key, value)

    await db.commit()
    await db.refresh(investor)
    return investor

# ✅ Slet en investor
async def delete_investor(db: AsyncSession, investor_id: int):
    investor = await get_investor_by_id(db, investor_id)
    if not investor:
        return None
    
    await db.delete(investor)
    await db.commit()
    return investor

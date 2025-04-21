from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.investment import Investment
from schemas.investment import InvestmentCreate, InvestmentResponse

# ✅ Opret en ny investering
async def create_investment(db: AsyncSession, investment_data: InvestmentCreate) -> Investment:
    db_investment = Investment(**investment_data.dict())
    db.add(db_investment)
    await db.commit()
    await db.refresh(db_investment)
    return db_investment

async def get_investments(db: AsyncSession, investor_id: int):
    print(f"🔍 Fetching investments for investor_id: {investor_id}")  # Debug log
    result = await db.execute(select(Investment).filter(Investment.investor_id == investor_id))
    investments = result.scalars().all()
    print(f"✅ Investments found in DB: {investments}")  # Debug log
    return investments


# ✅ Hent en investering via ID
async def get_investment_by_id(db: AsyncSession, investment_id: int):
    result = await db.execute(select(Investment).where(Investment.id == investment_id))
    return result.scalars().first()

# ✅ Slet en investering
async def delete_investment(db: AsyncSession, investment_id: int):
    investment = await get_investment_by_id(db, investment_id)
    if not investment:
        return None
    
    await db.delete(investment)
    await db.commit()
    return investment

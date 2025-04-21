from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.company import Company
from schemas.company import CompanyCreate, CompanyResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Opret en ny virksomhed
async def create_company(db: AsyncSession, company: CompanyCreate) -> Company:
    hashed_pw = pwd_context.hash(company.password)  
    data = company.dict(exclude_unset=True)
    data["password"] = hashed_pw
    db_company = Company(**data)
    
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    
    return db_company

# ✅ Hent alle virksomheder
async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()

# ✅ Hent en virksomhed via ID
async def get_company_by_id(db: AsyncSession, company_id: int):
    result = await db.execute(select(Company).where(Company.id == company_id))
    return result.scalars().first()

# ✅ Hent en virksomhed baseret på email
async def get_company_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Company).where(Company.business_email == email))
    return result.scalars().first()

# ✅ Opdater en virksomhed
async def update_company(db: AsyncSession, company_id: int, company_update: CompanyCreate):
    company = await get_company_by_id(db, company_id)
    if not company:
        return None
    
    for key, value in company_update.dict(exclude_unset=True).items():
        setattr(company, key, value)

    await db.commit()
    await db.refresh(company)
    return company

# ✅ Slet en virksomhed
async def delete_company(db: AsyncSession, company_id: int):
    company = await get_company_by_id(db, company_id)
    if not company:
        return None
    
    await db.delete(company)
    await db.commit()
    return company

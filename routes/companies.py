from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from crud.company import (
    create_company, get_companies, get_company_by_id, delete_company, update_company
)
from schemas.company import CompanyCreate, CompanyResponse
from models.company import Company
from routes.auth import get_current_user

router = APIRouter()

# ✅ Opret en virksomhed
@router.post("/", response_model=CompanyResponse)
async def create_new_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    return await create_company(db, company)

# ✅ Hent alle virksomheder
@router.get("/", response_model=list[CompanyResponse])
async def get_all_companies(db: AsyncSession = Depends(get_db)):
    return await get_companies(db)

# ✅ Hent en virksomhed via ID
@router.get("/{company_id}", response_model=CompanyResponse)
async def get_single_company(company_id: int, db: AsyncSession = Depends(get_db)):
    company = await get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# ✅ Opdater virksomhedens profil
@router.put("/update-profile")
async def update_company_profile(
    company_update: CompanyCreate, db: AsyncSession = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    company = await get_company_by_id(db, current_user.id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    updated_company = await update_company(db, current_user.id, company_update)
    if not updated_company:
        raise HTTPException(status_code=500, detail="Could not update company")
    
    return {"message": "Company profile updated successfully"}

# ✅ Slet en virksomhed
@router.delete("/{company_id}")
async def delete_single_company(company_id: int, db: AsyncSession = Depends(get_db)):
    company = await delete_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": f"Company {company.business_email} deleted successfully!"}

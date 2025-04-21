from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from crud.investor import (
    create_investor, get_investors, get_investor_by_id, delete_investor, update_investor
)
from schemas.investor import InvestorCreate, InvestorResponse
from models.investor import Investor
from models.investor_profile import InvestorProfile
from schemas.investor_profile import InvestorProfileResponse
from routes.auth import get_current_user
from typing import List, Optional
from sqlalchemy.future import select

router = APIRouter()

# ✅ Opret en investor
@router.post("/", response_model=InvestorResponse)
async def create_new_investor(investor: InvestorCreate, db: AsyncSession = Depends(get_db)):
    return await create_investor(db, investor)

# ✅ Søg efter investorer baseret på kriterier
@router.get("/search", response_model=List[InvestorProfileResponse])
async def search_investors(
    db: AsyncSession = Depends(get_db),
    sector: Optional[str] = Query(None),
    min_investment: Optional[int] = Query(None),
    impact_focus: Optional[str] = Query(None),
    risk_profile: Optional[str] = Query(None)
):
    query = select(
        InvestorProfile.id,  
        InvestorProfile.investor_id,
        Investor.firstname,
        Investor.lastname,
        InvestorProfile.preferred_sectors,
        InvestorProfile.investment_range_min,
        InvestorProfile.impact_focus,
        InvestorProfile.risk_profile
    ).join(Investor)

    if sector:
        query = query.where(InvestorProfile.preferred_sectors.ilike(f"%{sector}%"))
    if min_investment:
        query = query.where(InvestorProfile.investment_range_min >= min_investment)
    if impact_focus:
        query = query.where(InvestorProfile.impact_focus.ilike(f"%{impact_focus}%"))
    if risk_profile:
        query = query.where(InvestorProfile.risk_profile == risk_profile)

    result = await db.execute(query)
    investors = result.mappings().all()

    return investors

# ✅ Hent alle investorer
@router.get("/", response_model=List[InvestorResponse])
async def get_all_investors(db: AsyncSession = Depends(get_db)):
    return await get_investors(db)

# ✅ Hent en investor via ID
@router.get("/{investor_id}", response_model=InvestorResponse)
async def get_single_investor(investor_id: int, db: AsyncSession = Depends(get_db)):
    investor = await get_investor_by_id(db, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor

# ✅ Opdater investorens profil
@router.put("/update-profile")
async def update_investor_profile(
    investor_update: InvestorCreate, db: AsyncSession = Depends(get_db),
    current_user: Investor = Depends(get_current_user)
):
    investor = await get_investor_by_id(db, current_user.id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    updated_investor = await update_investor(db, current_user.id, investor_update)
    if not updated_investor:
        raise HTTPException(status_code=500, detail="Could not update investor")
    
    return {"message": "Investor profile updated successfully"}

# ✅ Slet en investor
@router.delete("/{investor_id}")
async def delete_single_investor(investor_id: int, db: AsyncSession = Depends(get_db)):
    investor = await delete_investor(db, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return {"message": f"Investor {investor.email} deleted successfully!"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from crud.investor_profile import (
    create_investor_profile, get_investor_profile_by_investor_id, update_investor_profile
)
from schemas.investor_profile import InvestorProfileCreate, InvestorProfileResponse
from models.investor import Investor
from routes.auth import get_current_user

router = APIRouter()

# ✅ Opret en investor-profil
@router.post("/", response_model=InvestorProfileResponse)
async def create_new_investor_profile(profile: InvestorProfileCreate, db: AsyncSession = Depends(get_db), current_user: Investor = Depends(get_current_user)):
    profile.investor_id = current_user.id  # Sikrer, at profilen er knyttet til investoren
    return await create_investor_profile(db, profile)

# ✅ Hent en investor-profil via investor_id
@router.get("/", response_model=InvestorProfileResponse)
async def get_investor_profile(db: AsyncSession = Depends(get_db), current_user: Investor = Depends(get_current_user)):
    profile = await get_investor_profile_by_investor_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Investor profile not found")
    return profile

# ✅ Opdater en investor-profil
@router.put("/")
async def update_profile_data(
    profile_update: InvestorProfileCreate, db: AsyncSession = Depends(get_db), current_user: Investor = Depends(get_current_user)
):
    profile = await get_investor_profile_by_investor_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Investor profile not found")

    updated_profile = await update_investor_profile(db, current_user.id, profile_update)
    return updated_profile

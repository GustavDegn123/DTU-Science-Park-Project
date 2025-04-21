from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from crud.matchmaking import (
    create_matchmaking, get_matchmakings, get_matchmaking_by_id, delete_matchmaking
)
from schemas.matchmaking import MatchmakingCreate, MatchmakingResponse, MatchmakingBase
from models.investor import Investor
from models.company import Company
from routes.auth import get_current_user
from sqlalchemy.future import select
from models.startup import Startup
from schemas.startup import StartupResponse
from typing import List
from models.matchmaking import Matchmaking
from schemas.investor import InvestorResponse
from models.investor_profile import InvestorProfile
from schemas.investor_profile import InvestorProfileResponse

router = APIRouter()

@router.get("/search-startups")
async def search_startups(
    db: AsyncSession = Depends(get_db),
    sector: str = Query(None),
    funding_stage: str = Query(None),
    revenue: int = Query(None),
    employees: int = Query(None),
    esg_score: int = Query(None),
    traction: int = Query(None)
):
    query = select(Startup)

    if sector:
        query = query.where(Startup.sector.ilike(f"%{sector}%"))
    if funding_stage:
        query = query.where(Startup.funding_stage.ilike(f"%{funding_stage}%"))
    if revenue:
        query = query.where(Startup.revenue.between(revenue * 0.9, revenue * 1.1))  # ±10% fleksibilitet
    if employees:
        query = query.where(Startup.employees.between(employees * 0.9, employees * 1.1))  # ±10% fleksibilitet
    if esg_score:
        query = query.where(Startup.esg_score >= esg_score)  # Minimumskrav til ESG
    if traction:
        query = query.where(Startup.traction >= traction)  # Minimumskrav til Traction

    result = await db.execute(query)
    startups = result.scalars().all()

    return startups

@router.post("/", response_model=MatchmakingResponse)
async def create_new_matchmaking(
    matchmaking: MatchmakingBase,  # 👈 Modtager kun startup_id og match_score
    db: AsyncSession = Depends(get_db), 
    current_user: Investor = Depends(get_current_user)  # 🔥 Henter investor fra token
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    new_match = await create_matchmaking(
        db,
        MatchmakingCreate(
            startup_id=matchmaking.startup_id,
            match_score=matchmaking.match_score,
            status=matchmaking.status,
            investor_id=current_user.id  # ✅ Sæt investor_id eksplicit
        )
    )

    return new_match

@router.get("/my-matches", response_model=List[StartupResponse])
async def get_my_matches(
    db: AsyncSession = Depends(get_db), 
    current_user: Investor = Depends(get_current_user)
):
    """ Henter alle startups, som en investor har matchet med. """
    query = select(Startup).join(Matchmaking).where(Matchmaking.investor_id == current_user.id)
    result = await db.execute(query)
    startups = result.scalars().all()
    return startups

@router.post("/match-investor", response_model=MatchmakingResponse)
async def match_investor(
    matchmaking: MatchmakingCreate,  # Brug MatchmakingCreate, da den har investor_id
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    print(f"DEBUG: Current user -> {current_user}")

    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Hvis brugeren er en startup, så laver de et match med en investor
    if isinstance(current_user, Company):
        startup_id = current_user.id
        investor_id = matchmaking.investor_id  # Kommer fra request body
    # Hvis brugeren er en investor, så laver de et match med en startup
    elif isinstance(current_user, Investor):
        startup_id = matchmaking.startup_id  # Kommer fra request body
        investor_id = current_user.id
    else:
        raise HTTPException(status_code=403, detail="Invalid user type for matchmaking")

    new_match = await create_matchmaking(
        db,
        MatchmakingCreate(
            startup_id=startup_id,
            match_score=matchmaking.match_score,
            status=matchmaking.status,
            investor_id=investor_id  
        )
    )

    return new_match

@router.get("/my-startup-matches", response_model=List[StartupResponse])
async def get_my_startup_matches(
    db: AsyncSession = Depends(get_db), 
    current_user: Investor = Depends(get_current_user)
):
    """ Henter alle startups, som en investor har matchet med. """
    query = select(Startup).join(Matchmaking).where(Matchmaking.investor_id == current_user.id)
    result = await db.execute(query)
    startups = result.scalars().all()
    return startups

@router.get("/my-matched-investors", response_model=List[InvestorProfileResponse])
async def get_my_matched_investors(
    db: AsyncSession = Depends(get_db), 
    current_user: Company = Depends(get_current_user)
):
    """ Henter alle investorer, som en startup har matchet med, inkl. deres investorprofil. """
    query = (
        select(
            InvestorProfile.id.label("id"),  # 👈 Tilføj ID fra InvestorProfile
            Investor.id.label("investor_id"),  
            Investor.firstname,
            Investor.lastname,
            InvestorProfile.preferred_sectors,
            InvestorProfile.impact_focus,
            InvestorProfile.investment_range_min,
            InvestorProfile.investment_range_max,
            InvestorProfile.risk_profile
        )
        .join(Matchmaking, Matchmaking.investor_id == Investor.id)
        .outerjoin(InvestorProfile, InvestorProfile.investor_id == Investor.id)  
        .where(Matchmaking.startup_id == current_user.id)
    )

    result = await db.execute(query)
    investors = result.mappings().all()

    # ✅ Formatér output korrekt
    formatted_investors = [
        {
            "id": inv["id"],  # 🔥 Tilføj id til responsen
            "investor_id": inv["investor_id"],
            "firstname": inv["firstname"],
            "lastname": inv["lastname"],
            "preferred_sectors": inv["preferred_sectors"],
            "impact_focus": inv["impact_focus"],
            "investment_range_min": inv["investment_range_min"],
            "investment_range_max": inv["investment_range_max"],
            "risk_profile": inv["risk_profile"]
        } for inv in investors
    ]

    return formatted_investors

# ✅ Hent alle matchmakings
@router.get("/", response_model=list[MatchmakingResponse])
async def get_all_matchmakings(db: AsyncSession = Depends(get_db)):
    return await get_matchmakings(db)

# ✅ Hent en matchmaking via ID
@router.get("/{matchmaking_id}", response_model=MatchmakingResponse)
async def get_single_matchmaking(matchmaking_id: int, db: AsyncSession = Depends(get_db)):
    matchmaking = await get_matchmaking_by_id(db, matchmaking_id)
    if not matchmaking:
        raise HTTPException(status_code=404, detail="Matchmaking not found")
    return matchmaking

# ✅ Slet en matchmaking
@router.delete("/{matchmaking_id}")
async def delete_single_matchmaking(matchmaking_id: int, db: AsyncSession = Depends(get_db), current_user: Investor = Depends(get_current_user)):
    matchmaking = await get_matchmaking_by_id(db, matchmaking_id)
    if not matchmaking or matchmaking.investor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this matchmaking")

    await delete_matchmaking(db, matchmaking_id)
    return {"message": f"Matchmaking {matchmaking.id} deleted successfully!"}

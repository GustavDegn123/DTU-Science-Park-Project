from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from crud.investment import (
    create_investment, get_investments, get_investment_by_id, delete_investment
)
from schemas.investment import InvestmentCreate, InvestmentResponse
from models.investor import Investor
from models.investment import Investment
from routes.auth import get_current_user
from sqlalchemy.future import select  
from models.company import Company

router = APIRouter()

@router.post("/", response_model=InvestmentResponse)
async def create_new_investment(
    investment_data: InvestmentCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: Investor = Depends(get_current_user)
):
    if not isinstance(current_user, Investor):
        raise HTTPException(status_code=403, detail="Only investors can create investments")

    new_investment = Investment(
        investor_id=current_user.id,  
        startup_id=investment_data.startup_id,
        amount=investment_data.amount
    )

    db.add(new_investment)
    await db.commit()
    await db.refresh(new_investment)
    return new_investment

@router.get("/", response_model=list[InvestmentResponse])
async def get_all_investments_for_investor(
    db: AsyncSession = Depends(get_db), 
    current_user: Investor = Depends(get_current_user)
):
    investments = await get_investments(db, investor_id=current_user.id)  # Brug korrekt funktion
    return investments

@router.get("/company-investments", response_model=list[InvestmentResponse])
async def get_company_received_investments(
    db: AsyncSession = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """ Henter investeringer for startups ejet af den aktuelle virksomhed """
    from models.startup import Startup  

    # Hent startups ejet af denne virksomhed
    result = await db.execute(select(Startup.id, Startup.name).where(Startup.company_id == current_user.id))
    startups = result.all()

    if not startups:
        return []  # Ingen startups → ingen investeringer

    # Omdan til dictionary {id: name}
    startup_dict = {row[0]: row[1] for row in startups}

    # Hent investeringer i disse startups
    investments_result = await db.execute(
        select(Investment).where(Investment.startup_id.in_(startup_dict.keys()))
    )
    investments = investments_result.scalars().all()

    # Tilføj startup-navn til investment-objekterne
    return [
        InvestmentResponse(
            id=inv.id,
            investor_id=inv.investor_id,
            startup_id=inv.startup_id,
            startup_name=startup_dict.get(inv.startup_id, "Unknown Startup"),  # ✅ Tilføj startup-navn
            amount=inv.amount,
            investment_date=inv.investment_date
        )
        for inv in investments
    ]

@router.delete("/{investment_id}")
async def delete_single_investment(
    investment_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: Investor = Depends(get_current_user)
):
    investment = await get_investment_by_id(db, investment_id)
    if not investment or investment.investor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this investment")

    await delete_investment(db, investment_id)
    return {"message": f"Investment {investment.id} deleted successfully!"}

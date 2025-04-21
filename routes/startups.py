from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from crud.startup import (
    create_startup, get_startups, get_startup_by_id, update_startup, delete_startup
)
from schemas.startup import StartupCreate, StartupResponse
from models.company import Company
from routes.auth import get_current_user
from models.startup import Startup
from sqlalchemy.future import select  

router = APIRouter()

# ✅ Opret en startup
@router.post("/", response_model=StartupResponse)
async def create_new_startup(startup: StartupCreate, db: AsyncSession = Depends(get_db), current_user: Company = Depends(get_current_user)):
    startup.company_id = current_user.id  # Sikrer, at startup er knyttet til virksomheden
    return await create_startup(db, startup)

@router.get("/", response_model=list[StartupResponse])
async def get_all_startups(db: AsyncSession = Depends(get_db)):
    startups = await get_startups(db)  # Brug get_startups-funktionen her
    if not startups:
        raise HTTPException(status_code=404, detail="No startups found")
    return startups

@router.get("/my-startups", response_model=list[StartupResponse])
async def get_my_startups(db: AsyncSession = Depends(get_db), current_user: Company = Depends(get_current_user)):
    """ Henter alle startups, som en virksomhed har oprettet """
    result = await db.execute(select(Startup).where(Startup.company_id == current_user.id))
    startups = result.scalars().all()

    return startups  # Returnér startups direkte uden en HTTPException, da [] er en valid tom liste

# ✅ Hent en startup via ID
@router.get("/{startup_id}", response_model=StartupResponse)
async def get_single_startup(startup_id: int, db: AsyncSession = Depends(get_db)):
    startup = await get_startup_by_id(db, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup

# ✅ Opdater en startup
@router.put("/{startup_id}")
async def update_startup_data(
    startup_id: int, startup_update: StartupCreate, db: AsyncSession = Depends(get_db), current_user: Company = Depends(get_current_user)
):
    startup = await get_startup_by_id(db, startup_id)
    if not startup or startup.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this startup")

    updated_startup = await update_startup(db, startup_id, startup_update)
    return updated_startup

# ✅ Slet en startup
@router.delete("/{startup_id}")
async def delete_single_startup(startup_id: int, db: AsyncSession = Depends(get_db), current_user: Company = Depends(get_current_user)):
    startup = await delete_startup(db, startup_id)
    if not startup or startup.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this startup")
    
    return {"message": f"Startup '{startup.name}' deleted successfully!"}

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from services.impact_scoring import calculate_impact_score
from services.impact_scoring import update_impact_scores

router = APIRouter()

@router.get("/impact-scores")
async def get_impact_scores(db: AsyncSession = Depends(get_db)):
    """
    API-endpoint der returnerer beregnede impact scores for startups fra databasen.
    """
    scores = await calculate_impact_score(db)
    return {"impact_scores": scores}

@router.post("/update-impact-scores")
async def update_and_store_impact_scores(db: AsyncSession = Depends(get_db)):
    """
    API-endpoint der beregner og gemmer impact scores i databasen.
    """
    response = await update_impact_scores(db)
    return response



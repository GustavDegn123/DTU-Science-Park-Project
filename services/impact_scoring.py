from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.startup import Startup
import pandas as pd

async def calculate_impact_score(db: AsyncSession):
    """
    Henter startups fra databasen og beregner deres impact score.
    """
    result = await db.execute(select(Startup))
    startups = result.scalars().all()

    if not startups:
        return []

    # Konverter startups til dictionary liste
    startup_list = [
        {
            "id": s.id,
            "name": s.name,
            "esg_score": s.esg_score or 0,
            "traction": s.traction or 0,
            "team": 70,  # Hardcoded midlertidigt (kan hentes senere)
            "funding_history": s.funding_history or 0,
            "sdg_alignment": s.sdg_alignment or 0
        }
        for s in startups
    ]

    df = pd.DataFrame(startup_list)

    # Definer vægtning af faktorer i Impact Score
    weights = {
        "esg_score": 0.30,
        "traction": 0.25,
        "team": 0.20,
        "funding_history": 0.15,
        "sdg_alignment": 0.10
    }

    # Beregn Impact Score
    df["impact_score"] = (
        df["esg_score"] * weights["esg_score"] +
        df["traction"] * weights["traction"] +
        df["team"] * weights["team"] +
        df["funding_history"] * weights["funding_history"] +
        df["sdg_alignment"] * weights["sdg_alignment"]
    )

    return df.to_dict(orient="records")

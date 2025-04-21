from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StartupBase(BaseModel):
    name: str
    description: str
    sector: Optional[str] = None
    funding_stage: Optional[str] = None
    revenue: Optional[float] = None
    employees: Optional[int] = None
    funding_goal: Optional[float] = None
    impact_score: Optional[float] = None
    esg_score: Optional[float] = None
    traction: Optional[float] = None
    funding_history: Optional[float] = None
    sdg_alignment: Optional[float] = None
    funding_sought: Optional[float] = 0
    funding_received: Optional[float] = 0

class StartupCreate(StartupBase):
    company_id: int

class StartupResponse(StartupBase):
    id: int
    created_at: datetime
    funding_needed: float

    class Config:
        orm_mode = True

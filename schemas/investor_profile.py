from pydantic import BaseModel
from typing import Optional


class InvestorProfileBase(BaseModel):
    investor_type: Optional[str] = None
    preferred_sectors: Optional[str] = None
    impact_focus: Optional[str] = None
    investment_range_min: Optional[float] = None
    investment_range_max: Optional[float] = None
    risk_profile: Optional[str] = None
    preferred_esg_score: Optional[float] = None


class InvestorProfileCreate(InvestorProfileBase):
    investor_id: int


class InvestorProfileResponse(InvestorProfileBase):
    id: int
    investor_id: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None

    class Config:
        from_attributes = True  # FastAPI 0.95+ bruger "from_attributes" i stedet for "orm_mode"

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InvestmentBase(BaseModel):
    startup_id: int
    amount: float

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentResponse(InvestmentBase):
    id: int
    investor_id: int
    investment_date: datetime
    startup_name: Optional[str] = None  # ✅ Gør startup_name valgfrit

    class Config:
        orm_mode = True

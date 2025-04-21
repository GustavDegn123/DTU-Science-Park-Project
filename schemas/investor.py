from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class InvestorBase(BaseModel):
    name: str
    email: EmailStr
    country: Optional[str] = None
    firstname: str
    lastname: str

class InvestorCreate(InvestorBase):
    password: str

class InvestorResponse(InvestorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

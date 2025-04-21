from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    business_email: EmailStr
    country: Optional[str] = None
    firstname: str
    lastname: str

class CompanyCreate(CompanyBase):
    password: str

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

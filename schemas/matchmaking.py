from pydantic import BaseModel
from datetime import datetime

class MatchmakingBase(BaseModel):
    startup_id: int
    match_score: float
    status: str = "Pending"

class MatchmakingCreate(MatchmakingBase):
  investor_id: int

class MatchmakingResponse(MatchmakingBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

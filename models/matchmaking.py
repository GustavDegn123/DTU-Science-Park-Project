from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.sql import func

class Matchmaking(Base):
    __tablename__ = "matchmaking"
    
    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investors.id", ondelete="CASCADE"), nullable=False)
    startup_id = Column(Integer, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False)
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    investor = relationship("Investor", back_populates="matchmaking")
    startup = relationship("Startup", back_populates="matchmaking")

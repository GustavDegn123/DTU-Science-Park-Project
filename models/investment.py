from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.sql import func
from datetime import datetime

class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investors.id", ondelete="CASCADE"), nullable=False)
    startup_id = Column(Integer, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    investment_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    investor = relationship("Investor", back_populates="investments")
    startup = relationship("Startup", back_populates="investments")

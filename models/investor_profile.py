# models/investor_profile.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class InvestorProfile(Base):
    __tablename__ = "investor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investors.id", ondelete="CASCADE"), nullable=False, unique=True)
    investor_type = Column(String(50))
    preferred_sectors = Column(String(255))  # Kan være en liste i fremtiden
    impact_focus = Column(String(50))
    investment_range_min = Column(Float)
    investment_range_max = Column(Float)
    risk_profile = Column(String(50))
    preferred_esg_score = Column(Float)

    investor = relationship("Investor", back_populates="profile")

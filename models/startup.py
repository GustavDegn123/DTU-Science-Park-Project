from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

class Startup(Base):
    __tablename__ = "startups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    sector = Column(String(100))
    funding_stage = Column(String(50))
    revenue = Column(Float)
    employees = Column(Integer)
    funding_goal = Column(Float)
    impact_score = Column(Float)
    esg_score = Column(Float)
    traction = Column(Float)
    funding_history = Column(Float)
    sdg_alignment = Column(Float)
    funding_sought = Column(Float, nullable=False, default=0)
    funding_received = Column(Float, nullable=False, default=0)

    @hybrid_property
    def funding_needed(self):
        return self.funding_sought - self.funding_received

    # Relation til virksomheden, der ejer startup'en
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", back_populates="startups")
    investments = relationship("Investment", back_populates="startup")
    matchmaking = relationship("Matchmaking", back_populates="startup") 

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

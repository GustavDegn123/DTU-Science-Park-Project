# models/investor.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.sql import func

class Investor(Base):
    __tablename__ = "investors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    country = Column(String(50))
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationer
    investments = relationship("Investment", back_populates="investor")
    matchmaking = relationship("Matchmaking", back_populates="investor")
    profile = relationship("InvestorProfile", uselist=False, back_populates="investor")  # Én-til-én relation

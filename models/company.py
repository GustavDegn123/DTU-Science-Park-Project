from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.sql import func

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    business_email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(Text, nullable=False)
    country = Column(String(50))
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relation til startups
    startups = relationship("Startup", back_populates="company")

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.app.database import Base
from .calculation import Calculation  # Import the calculation model for relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship with calculations
    calculations = relationship("Calculation", back_populates="owner", cascade="all, delete-orphan")

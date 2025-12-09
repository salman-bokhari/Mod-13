from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)  # <-- add this
    password = Column(String, nullable=False)

    calculations = relationship("Calculation", back_populates="user")

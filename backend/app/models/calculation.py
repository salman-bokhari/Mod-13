from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .user import User
from ..database import Base

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    operand1 = Column(Float, nullable=False)
    operand2 = Column(Float, nullable=False)
    operation = Column(String, nullable=False)
    result = Column(Float, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="calculations")

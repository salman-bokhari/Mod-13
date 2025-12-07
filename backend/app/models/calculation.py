from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, nullable=False)
    operand1 = Column(Float, nullable=False)
    operand2 = Column(Float, nullable=False)
    result = Column(Float, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="calculations")

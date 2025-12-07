from pydantic import BaseModel, Field
from typing import Optional

class CalculationBase(BaseModel):
    operation: str = Field(..., regex="^(add|subtract|multiply|divide)$")
    operand1: float
    operand2: float

class CalculationCreate(CalculationBase):
    pass

class CalculationUpdate(BaseModel):
    operation: Optional[str] = Field(None, regex="^(add|subtract|multiply|divide)$")
    operand1: Optional[float]
    operand2: Optional[float]

class CalculationOut(CalculationBase):
    id: int
    result: float

    class Config:
        orm_mode = True
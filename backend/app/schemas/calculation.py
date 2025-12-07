from pydantic import BaseModel

class CalculationBase(BaseModel):
    operation: str
    operand1: float
    operand2: float

class CalculationCreate(CalculationBase):
    pass

class CalculationUpdate(BaseModel):
    operation: str | None = None
    operand1: float | None = None
    operand2: float | None = None
    result: float | None = None

class CalculationRead(CalculationBase):
    id: int
    result: float
    owner_id: int

    class Config:
        orm_mode = True

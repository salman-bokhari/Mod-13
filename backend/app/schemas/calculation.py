from pydantic import BaseModel

class CalculationCreate(BaseModel):
    operand1: float
    operand2: float
    operation: str

    class Config:
        orm_mode = True

class CalculationOut(BaseModel):
    id: int
    operand1: float
    operand2: float
    operation: str
    result: float

    class Config:
        orm_mode = True

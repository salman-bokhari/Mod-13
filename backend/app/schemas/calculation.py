from pydantic import BaseModel

class CalculationCreate(BaseModel):
    operand1: float
    operand2: float
    operation: str

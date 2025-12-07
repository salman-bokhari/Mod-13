from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.calculation import Calculation
from backend.app.models.user import User
from backend.app.auth_utils import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/calculations", tags=["calculations"])

# ---- Request Model ----
class CalculationCreate(BaseModel):
    operand1: int
    operand2: int
    operation: str

# ---- Create ----
@router.post("", response_model=dict)
def create_calculation(payload: CalculationCreate,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):

    if payload.operation == "add":
        result = payload.operand1 + payload.operand2
    elif payload.operation == "subtract":
        result = payload.operand1 - payload.operand2
    elif payload.operation == "multiply":
        result = payload.operand1 * payload.operand2
    elif payload.operation == "divide":
        if payload.operand2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = payload.operand1 / payload.operand2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    calc = Calculation(
        operand1=payload.operand1,
        operand2=payload.operand2,
        operation=payload.operation,
        result=result,
        user_id=current_user.id
    )

    db.add(calc)
    db.commit()
    db.refresh(calc)

    return {
        "id": calc.id,
        "operand1": calc.operand1,
        "operand2": calc.operand2,
        "operation": calc.operation,
        "result": calc.result
    }


# ---- Browse ----
@router.get("")
def list_calculations(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return db.query(Calculation).filter(Calculation.user_id == current_user.id).all()


# ---- Edit ----
@router.put("/{calc_id}")
def update_calculation(calc_id: int,
                       payload: CalculationCreate,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):

    calc = db.query(Calculation).filter(
        Calculation.id == calc_id,
        Calculation.user_id == current_user.id
    ).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Not found")

    calc.operand1 = payload.operand1
    calc.operand2 = payload.operand2
    calc.operation = payload.operation

    if payload.operation == "add":
        calc.result = payload.operand1 + payload.operand2
    elif payload.operation == "subtract":
        calc.result = payload.operand1 - payload.operand2
    elif payload.operation == "multiply":
        calc.result = payload.operand1 * payload.operand2
    elif payload.operation == "divide":
        if payload.operand2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        calc.result = payload.operand1 / payload.operand2

    db.commit()
    db.refresh(calc)

    return calc


# ---- Delete ----
@router.delete("/{calc_id}")
def delete_calculation(calc_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):

    calc = db.query(Calculation).filter(
        Calculation.id == calc_id,
        Calculation.user_id == current_user.id
    ).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(calc)
    db.commit()

    return {"deleted": True}

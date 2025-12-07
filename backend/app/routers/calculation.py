from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.calculation import Calculation
from backend.app.models.user import User
from backend.app.schemas.calculation import CalculationCreate, CalculationUpdate, CalculationOut
from backend.app.auth import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])

def compute_result(operation, op1, op2):
    if operation == "add":
        return op1 + op2
    elif operation == "subtract":
        return op1 - op2
    elif operation == "multiply":
        return op1 * op2
    elif operation == "divide":
        if op2 == 0:
            raise ValueError("Cannot divide by zero")
        return op1 / op2
    else:
        raise ValueError("Invalid operation")

# Browse all
@router.get("/", response_model=list[CalculationOut])
def browse_calculations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Calculation).filter(Calculation.user_id == current_user.id).all()

# Read single
@router.get("/{calculation_id}", response_model=CalculationOut)
def read_calculation(calculation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calculation_id, Calculation.user_id == current_user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

# Add
@router.post("/", response_model=CalculationOut)
def add_calculation(data: CalculationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = compute_result(data.operation, data.operand1, data.operand2)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    calc = Calculation(user_id=current_user.id, operation=data.operation, operand1=data.operand1, operand2=data.operand2, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

# Edit
@router.put("/{calculation_id}", response_model=CalculationOut)
def update_calculation(calculation_id: int, data: CalculationUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calculation_id, Calculation.user_id == current_user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if data.operation:
        calc.operation = data.operation
    if data.operand1 is not None:
        calc.operand1 = data.operand1
    if data.operand2 is not None:
        calc.operand2 = data.operand2
    try:
        calc.result = compute_result(calc.operation, calc.operand1, calc.operand2)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    db.commit()
    db.refresh(calc)
    return calc

# Delete
@router.delete("/{calculation_id}", response_model=dict)
def delete_calculation(calculation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calculation_id, Calculation.user_id == current_user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()
    return {"message": "Calculation deleted successfully"}

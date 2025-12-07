from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.calculation import Calculation
from backend.app.models.user import User
from backend.app.auth import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.post("/")
def add_calculation(data: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    operand1 = data.get("operand1")
    operand2 = data.get("operand2")
    operation = data.get("operation")
    
    if operation == "add":
        result = operand1 + operand2
    elif operation == "subtract":
        result = operand1 - operand2
    elif operation == "multiply":
        result = operand1 * operand2
    elif operation == "divide":
        result = operand1 / operand2 if operand2 != 0 else 0
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    calc = Calculation(operand1=operand1, operand2=operand2, operation=operation, result=result, owner_id=user.id)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

@router.get("/")
def browse_calculations(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Calculation).filter(Calculation.owner_id == user.id).all()

@router.get("/{calc_id}")
def read_calculation(calc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.owner_id == user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

@router.put("/{calc_id}")
def edit_calculation(calc_id: int, data: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.owner_id == user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    calc.operand1 = data.get("operand1", calc.operand1)
    calc.operand2 = data.get("operand2", calc.operand2)
    calc.operation = data.get("operation", calc.operation)
    
    # recalc result
    if calc.operation == "add":
        calc.result = calc.operand1 + calc.operand2
    elif calc.operation == "subtract":
        calc.result = calc.operand1 - calc.operand2
    elif calc.operation == "multiply":
        calc.result = calc.operand1 * calc.operand2
    elif calc.operation == "divide":
        calc.result = calc.operand1 / calc.operand2 if calc.operand2 != 0 else 0

    db.commit()
    db.refresh(calc)
    return calc

@router.delete("/{calc_id}")
def delete_calculation(calc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.owner_id == user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()
    return {"status": "deleted"}

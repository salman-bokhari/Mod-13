from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models.calculation import Calculation
from backend.app.schemas.calculation import CalculationCreate, CalculationRead, CalculationUpdate
from backend.app.routers.auth import get_current_user
from backend.app.models.user import User

router = APIRouter(prefix="/calculations", tags=["calculations"])

# Browse: GET /calculations
@router.get("/", response_model=List[CalculationRead])
def browse_calculations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Calculation).filter(Calculation.owner_id == current_user.id).all()

# Read: GET /calculations/{id}
@router.get("/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.owner_id == current_user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

# Add: POST /calculations
@router.post("/", response_model=CalculationRead)
def add_calculation(calc: CalculationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_calc = Calculation(**calc.dict(), owner_id=current_user.id)
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc

# Edit: PUT /calculations/{id}
@router.put("/{calc_id}", response_model=CalculationRead)
def edit_calculation(calc_id: int, calc_update: CalculationUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.owner_id == current_user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    for key, value in calc_update.dict(exclude_unset=True).items():
        setattr(calc, key, value)
    db.commit()
    db.refresh(calc)
    return calc

# Delete: DELETE /calculations/{id}
@router.delete("/{calc_id}", status_code=204)
def delete_calculation(calc_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id, Calculation.owner_id == current_user.id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()

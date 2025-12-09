from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.calculation import Calculation
from backend.app.models.user import User
from backend.app.schemas.calculation import CalculationCreate, CalculationOut
from fastapi.security import OAuth2PasswordBearer
from backend.app.utils.jwt_handler import decode_access_token

router = APIRouter(tags=["calculations"])  # no prefix here

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---- Auth Dependency ----
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# ---- CREATE ----
@router.post("/", response_model=CalculationOut)
def create_calculation(
    payload: CalculationCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    if payload.operation == "add":
        result = payload.operand1 + payload.operand2
    elif payload.operation == "subtract":
        result = payload.operand1 - payload.operand2
    elif payload.operation == "multiply":
        result = payload.operand1 * payload.operand2
    elif payload.operation == "divide":
        if payload.operand2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = payload.operand1 / payload.operand2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    calc = Calculation(
        operand1=payload.operand1,
        operand2=payload.operand2,
        operation=payload.operation,
        result=result,
        user_id=user.id
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

# ---- LIST ----
@router.get("/", response_model=list[CalculationOut])
def list_calculations(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Calculation).filter(Calculation.user_id == user.id).all()

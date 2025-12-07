from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.app import database
from backend.app.schemas.user import UserCreate, Token
from backend.app.models.user import User
from backend.app.utils import hash as hash_utils
from backend.app.utils import jwt_handler

router = APIRouter(tags=["auth"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Register endpoint
# -----------------------
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if not user_in.username:
        user_in.username = user_in.email.split("@")[0]

    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Email already registered"}
        )

    hashed = hash_utils.get_password_hash(user_in.password)
    user = User(email=user_in.email, username=user_in.username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = jwt_handler.create_access_token({"sub": str(user.id), "email": user.email})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"access_token": token, "token_type": "bearer", "message": "Registration successful"}
    )

# -----------------------
# Login endpoint
# -----------------------
@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not hash_utils.verify_password(user_in.password, user.hashed_password):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid credentials"}
        )

    token = jwt_handler.create_access_token({"sub": str(user.id), "email": user.email})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": token, "token_type": "bearer", "message": "Login successful"}
    )

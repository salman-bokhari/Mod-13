from fastapi import APIRouter, Depends, HTTPException, status
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

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Set username to email prefix if not provided
    if not user_in.username:
        user_in.username = user_in.email.split("@")[0]

    # Check if email is already registered
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash password and create user
    hashed_password = hash_utils.get_password_hash(user_in.password)
    user = User(email=user_in.email, username=user_in.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT token
    token = jwt_handler.create_access_token({"sub": str(user.id), "email": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Registration successful"
    }

@router.post("/login", response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()

    if not user or not hash_utils.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = jwt_handler.create_access_token({"sub": str(user.id), "email": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Login successful"
    }

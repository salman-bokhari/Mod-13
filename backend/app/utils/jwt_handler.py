# backend/app/utils/jwt_handler.py
import jwt
from datetime import datetime, timedelta
import os

JWT_SECRET = os.environ.get("JWT_SECRET", "secret")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

def decode_access_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

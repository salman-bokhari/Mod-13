import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretdevkey")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60*24*7))

def create_access_token(subject: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = subject.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None

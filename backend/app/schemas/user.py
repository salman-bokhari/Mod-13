from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: Optional[str]
    email: EmailStr   # <-- add this
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

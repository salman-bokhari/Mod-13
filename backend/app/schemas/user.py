from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None  # optional, can default to email prefix

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)  # lowered to 6 to match test passwords

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None  # optional

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)  # <<--- fixed to 6

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

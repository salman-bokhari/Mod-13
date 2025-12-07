from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)  # minimum 6 for tests

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

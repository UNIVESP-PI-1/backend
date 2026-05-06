from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class LoginSchema(BaseModel):
    email: str
    password: str
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True

class CategorySchema(BaseModel):
    id: Optional[int] = None
    name: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
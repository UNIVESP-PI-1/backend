from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str

class UserResponseSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

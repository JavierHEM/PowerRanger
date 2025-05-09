from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    nombres: str
    apellidos: str
    cargo: Optional[str] = None
    rut: str
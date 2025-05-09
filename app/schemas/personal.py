from typing import Optional
from pydantic import BaseModel, EmailStr

class PersonalBase(BaseModel):
    """Esquema base para personal DTP"""
    rut: str
    nombres: str
    apellidos: str
    email: Optional[EmailStr] = None
    cargo: Optional[str] = None
    activo: Optional[bool] = True

class PersonalCreate(PersonalBase):
    """Esquema para crear personal DTP"""
    pass

class PersonalUpdate(BaseModel):
    """Esquema para actualizar personal DTP"""
    rut: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    cargo: Optional[str] = None
    activo: Optional[bool] = None

class PersonalInDB(PersonalBase):
    """Esquema para personal DTP en la base de datos"""
    id_personal: int
    
    class Config:
        from_attributes = True

# Alias para la respuesta de la API
Personal = PersonalInDB

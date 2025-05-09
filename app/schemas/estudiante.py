from typing import Optional, List, Dict, Any
from datetime import date
from pydantic import BaseModel, EmailStr, Field

# Esquemas para Estudiante
class EstudianteBase(BaseModel):
    """Esquema base para estudiantes"""
    rut: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    fecha_nacimiento: date
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    semestre_actual: Optional[int] = None
    activo: Optional[bool] = True

class EstudianteCreate(EstudianteBase):
    """Esquema para crear estudiantes"""
    id_carrera: Optional[int] = None
    # Opcionalmente, podemos incluir discapacidades al crear un estudiante
    discapacidades: Optional[List[Dict[str, Any]]] = None

class EstudianteUpdate(BaseModel):
    """Esquema para actualizar estudiantes"""
    rut: Optional[str] = None
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    semestre_actual: Optional[int] = None
    activo: Optional[bool] = None
    id_carrera: Optional[int] = None

class EstudianteInDB(EstudianteBase):
    """Esquema para estudiantes en la base de datos"""
    id_estudiante: int
    fecha_ingreso_programa: Optional[date] = None
    id_carrera: Optional[int] = None
    
    class Config:
        from_attributes = True

# Alias para la respuesta de la API
Estudiante = EstudianteInDB

# Esquemas para Discapacidad/Condición
class DiscapacidadBase(BaseModel):
    """Esquema base para discapacidades/condiciones"""
    nombre: str
    descripcion: Optional[str] = None
    id_tipo_disc: Optional[int] = None

class DiscapacidadCreate(DiscapacidadBase):
    """Esquema para crear discapacidades/condiciones"""
    pass

class DiscapacidadUpdate(BaseModel):
    """Esquema para actualizar discapacidades/condiciones"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_tipo_disc: Optional[int] = None

class DiscapacidadInDB(DiscapacidadBase):
    """Esquema para discapacidades/condiciones en la base de datos"""
    id_discapacidad: int
    
    class Config:
        from_attributes = True

# Alias para la respuesta de la API
Discapacidad = DiscapacidadInDB

# Esquemas para Estudiante-Discapacidad (relación)
class EstudianteDiscapacidadBase(BaseModel):
    """Esquema base para la relación estudiante-discapacidad"""
    id_estudiante: int
    id_discapacidad: int
    fecha_diagnostico: Optional[date] = None
    certificado_url: Optional[str] = None
    observaciones: Optional[str] = None

class EstudianteDiscapacidadCreate(EstudianteDiscapacidadBase):
    """Esquema para crear relación estudiante-discapacidad"""
    pass

class EstudianteDiscapacidadUpdate(BaseModel):
    """Esquema para actualizar relación estudiante-discapacidad"""
    fecha_diagnostico: Optional[date] = None
    certificado_url: Optional[str] = None
    observaciones: Optional[str] = None

class EstudianteDiscapacidadInDB(EstudianteDiscapacidadBase):
    """Esquema para relación estudiante-discapacidad en la base de datos"""
    id_estudiante_discapacidad: int
    
    class Config:
        from_attributes = True

# Alias para la respuesta de la API
EstudianteDiscapacidad = EstudianteDiscapacidadInDB

# Esquemas para importación de datos
class EstudianteFUD(BaseModel):
    """Esquema para importación de datos desde planilla FUD"""
    rut: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    fecha_nacimiento: date
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    carrera: Optional[str] = None
    semestre: Optional[int] = None
    discapacidad: Optional[str] = None
    observaciones: Optional[str] = None

class ImportacionResultado(BaseModel):
    """Esquema para resultado de importación"""
    total_procesados: int
    creados: int
    actualizados: int
    errores: List[Dict[str, Any]] = []

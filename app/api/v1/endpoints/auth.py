from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.schemas.auth import Token, UserLogin, UserSignUp
from app.utils.supabase import get_supabase_client
from app.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

@router.post("/login", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Obtiene un token JWT para acceder a la API mediante OAuth2 (formulario)
    """
    supabase = get_supabase_client()
    
    try:
        # Autenticación con Supabase
        response = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password
        })
        
        # Crear nuestro propio token JWT (opcional, también podríamos usar el de Supabase)
        access_token = create_access_token(
            subject=response.user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/login/json", response_model=Token)
async def login_json(user_data: UserLogin) -> Any:
    """
    Obtiene un token JWT para acceder a la API mediante JSON
    """
    supabase = get_supabase_client()
    
    try:
        # Autenticación con Supabase
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })
        
        # Crear token JWT
        access_token = create_access_token(
            subject=response.user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=Token)
async def register_user(user_data: UserSignUp) -> Any:
    """
    Registra un nuevo usuario en el sistema
    """
    supabase = get_supabase_client()
    
    try:
        # Crear usuario en Supabase Auth con metadatos
        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "full_name": f"{user_data.nombres} {user_data.apellidos}",
                    "rut": user_data.rut,
                    "cargo": user_data.cargo or "Usuario nuevo"
                }
            }
        })
        
        user_id = auth_response.user.id
        
        # No necesitamos insertar manualmente en personal_dtp, el trigger lo hará
        
        # Crear token JWT
        access_token = create_access_token(
            subject=user_id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo registrar el usuario: {str(e)}",
        )


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)) -> Any:
    """
    Cierra la sesión del usuario actual
    """
    supabase = get_supabase_client()
    
    try:
        # Cerrar sesión con Supabase
        supabase.auth.sign_out()
        return {"message": "Sesión cerrada correctamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al cerrar sesión: {str(e)}",
        )
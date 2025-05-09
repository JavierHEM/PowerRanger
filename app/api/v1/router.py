from fastapi import APIRouter
from app.api.v1.endpoints import auth, personal, estudiantes

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["autenticación"])
api_router.include_router(personal.router, prefix="/personal", tags=["personal"])
api_router.include_router(estudiantes.router, prefix="/estudiantes", tags=["estudiantes"])
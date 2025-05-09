from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.deps import get_current_user
from app.schemas.personal import Personal, PersonalCreate, PersonalUpdate
from app.utils.supabase import get_supabase_client

router = APIRouter()

@router.get("/", response_model=List[Personal])
async def get_all_personal(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene la lista de personal DTP.
    Puede filtrarse por estado activo/inactivo.
    """
    supabase = get_supabase_client()
    
    try:
        query = supabase.table("personal_dtp").select("*")
        
        # Aplicar filtro de activo si se proporciona
        if activo is not None:
            query = query.eq("activo", activo)
            
        # Aplicar paginación
        response = query.range(skip, skip + limit - 1).execute()
        
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener personal: {str(e)}"
        )

@router.get("/{personal_id}", response_model=Personal)
async def get_personal_by_id(
    personal_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene un miembro del personal DTP por su ID.
    """
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("personal_dtp").select("*").eq("id_personal", personal_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personal con ID {personal_id} no encontrado"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener personal: {str(e)}"
        )

@router.post("/", response_model=Personal, status_code=status.HTTP_201_CREATED)
async def create_personal(
    personal_data: PersonalCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crea un nuevo miembro del personal DTP.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si ya existe un personal con el mismo RUT
        check_response = supabase.table("personal_dtp").select("*").eq("rut", personal_data.rut).execute()
        
        if check_response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un personal con el RUT {personal_data.rut}"
            )
        
        # Crear el nuevo personal
        response = supabase.table("personal_dtp").insert(personal_data.model_dump()).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear personal"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear personal: {str(e)}"
        )

@router.put("/{personal_id}", response_model=Personal)
async def update_personal(
    personal_id: int,
    personal_data: PersonalUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza un miembro del personal DTP.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si el personal existe
        check_response = supabase.table("personal_dtp").select("*").eq("id_personal", personal_id).execute()
        
        if not check_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personal con ID {personal_id} no encontrado"
            )
        
        # Si se actualiza el RUT, verificar que no exista otro personal con ese RUT
        if personal_data.rut:
            rut_check = supabase.table("personal_dtp").select("*").eq("rut", personal_data.rut).neq("id_personal", personal_id).execute()
            
            if rut_check.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro personal con el RUT {personal_data.rut}"
                )
        
        # Filtrar campos nulos para no sobrescribir con None
        update_data = {k: v for k, v in personal_data.model_dump().items() if v is not None}
        
        # Actualizar el personal
        response = supabase.table("personal_dtp").update(update_data).eq("id_personal", personal_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar personal"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar personal: {str(e)}"
        )

@router.delete("/{personal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personal(
    personal_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Elimina un miembro del personal DTP.
    En realidad, marca como inactivo en lugar de eliminar físicamente.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si el personal existe
        check_response = supabase.table("personal_dtp").select("*").eq("id_personal", personal_id).execute()
        
        if not check_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personal con ID {personal_id} no encontrado"
            )
        
        # Marcar como inactivo en lugar de eliminar
        supabase.table("personal_dtp").update({"activo": False}).eq("id_personal", personal_id).execute()
        
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar personal: {str(e)}"
        )

@router.get("/buscar/rut/{rut}", response_model=Personal)
async def get_personal_by_rut(
    rut: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Busca un miembro del personal DTP por su RUT.
    """
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("personal_dtp").select("*").eq("rut", rut).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personal con RUT {rut} no encontrado"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar personal por RUT: {str(e)}"
        )

from typing import List, Optional, Dict, Any
from datetime import date
import io

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from app.core.deps import get_current_user
from app.schemas.estudiante import (
    Estudiante, EstudianteCreate, EstudianteUpdate, 
    EstudianteDiscapacidad, EstudianteDiscapacidadCreate, EstudianteDiscapacidadUpdate,
    Discapacidad, EstudianteFUD, ImportacionResultado
)
from app.utils.supabase import get_supabase_client
from app.utils.excel import procesar_planilla_fud

router = APIRouter()

# Endpoints para Estudiantes
@router.get("/", response_model=List[Estudiante])
async def get_all_estudiantes(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    carrera: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene la lista de estudiantes.
    Puede filtrarse por estado activo/inactivo y carrera.
    """
    supabase = get_supabase_client()
    
    try:
        query = supabase.table("estudiante").select("*")
        
        # Aplicar filtros
        if activo is not None:
            query = query.eq("activo", activo)
            
        if carrera is not None:
            query = query.eq("id_carrera", carrera)
            
        # Aplicar paginación
        response = query.range(skip, skip + limit - 1).execute()
        
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estudiantes: {str(e)}"
        )

@router.get("/{estudiante_id}", response_model=Estudiante)
async def get_estudiante_by_id(
    estudiante_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene un estudiante por su ID.
    """
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("estudiante").select("*").eq("id_estudiante", estudiante_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {estudiante_id} no encontrado"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estudiante: {str(e)}"
        )

@router.post("/", response_model=Estudiante, status_code=status.HTTP_201_CREATED)
async def create_estudiante(
    estudiante_data: EstudianteCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crea un nuevo estudiante.
    Opcionalmente puede incluir discapacidades asociadas.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si ya existe un estudiante con el mismo RUT
        check_response = supabase.table("estudiante").select("*").eq("rut", estudiante_data.rut).execute()
        
        if check_response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un estudiante con el RUT {estudiante_data.rut}"
            )
        
        # Extraer discapacidades si existen
        discapacidades = None
        if hasattr(estudiante_data, 'discapacidades'):
            discapacidades = estudiante_data.discapacidades
            # Eliminar discapacidades del diccionario para la inserción del estudiante
            estudiante_dict = estudiante_data.model_dump(exclude={"discapacidades"})
        else:
            estudiante_dict = estudiante_data.model_dump()
        
        # Crear el nuevo estudiante
        response = supabase.table("estudiante").insert(estudiante_dict).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear estudiante"
            )
        
        nuevo_estudiante = response.data[0]
        
        # Si hay discapacidades, asociarlas al estudiante
        if discapacidades:
            for disc in discapacidades:
                disc_data = {
                    "id_estudiante": nuevo_estudiante["id_estudiante"],
                    "id_discapacidad": disc["id_discapacidad"],
                    "fecha_diagnostico": disc.get("fecha_diagnostico"),
                    "certificado_url": disc.get("certificado_url"),
                    "observaciones": disc.get("observaciones")
                }
                supabase.table("estudiante_discapacidad").insert(disc_data).execute()
            
        return nuevo_estudiante
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear estudiante: {str(e)}"
        )

@router.put("/{estudiante_id}", response_model=Estudiante)
async def update_estudiante(
    estudiante_id: int,
    estudiante_data: EstudianteUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza un estudiante existente.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si el estudiante existe
        check_response = supabase.table("estudiante").select("*").eq("id_estudiante", estudiante_id).execute()
        
        if not check_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {estudiante_id} no encontrado"
            )
        
        # Si se actualiza el RUT, verificar que no exista otro estudiante con ese RUT
        if estudiante_data.rut:
            rut_check = supabase.table("estudiante").select("*").eq("rut", estudiante_data.rut).neq("id_estudiante", estudiante_id).execute()
            
            if rut_check.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro estudiante con el RUT {estudiante_data.rut}"
                )
        
        # Filtrar campos nulos para no sobrescribir con None
        update_data = {k: v for k, v in estudiante_data.model_dump().items() if v is not None}
        
        # Actualizar el estudiante
        response = supabase.table("estudiante").update(update_data).eq("id_estudiante", estudiante_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar estudiante"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar estudiante: {str(e)}"
        )

@router.delete("/{estudiante_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estudiante(
    estudiante_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Elimina un estudiante.
    En realidad, marca como inactivo en lugar de eliminar físicamente.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si el estudiante existe
        check_response = supabase.table("estudiante").select("*").eq("id_estudiante", estudiante_id).execute()
        
        if not check_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {estudiante_id} no encontrado"
            )
        
        # Marcar como inactivo en lugar de eliminar
        supabase.table("estudiante").update({"activo": False}).eq("id_estudiante", estudiante_id).execute()
        
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar estudiante: {str(e)}"
        )

@router.get("/buscar/rut/{rut}", response_model=Estudiante)
async def get_estudiante_by_rut(
    rut: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Busca un estudiante por su RUT.
    """
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("estudiante").select("*").eq("rut", rut).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con RUT {rut} no encontrado"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar estudiante por RUT: {str(e)}"
        )

# Endpoints para Discapacidades de Estudiantes
@router.get("/{estudiante_id}/discapacidades", response_model=List[EstudianteDiscapacidad])
async def get_discapacidades_estudiante(
    estudiante_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene las discapacidades asociadas a un estudiante.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si el estudiante existe
        check_estudiante = supabase.table("estudiante").select("*").eq("id_estudiante", estudiante_id).execute()
        
        if not check_estudiante.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {estudiante_id} no encontrado"
            )
        
        # Obtener discapacidades del estudiante
        response = supabase.table("estudiante_discapacidad").select("*").eq("id_estudiante", estudiante_id).execute()
        
        return response.data
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener discapacidades del estudiante: {str(e)}"
        )

@router.post("/{estudiante_id}/discapacidades", response_model=EstudianteDiscapacidad, status_code=status.HTTP_201_CREATED)
async def add_discapacidad_estudiante(
    estudiante_id: int,
    discapacidad_data: EstudianteDiscapacidadCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Asocia una discapacidad a un estudiante.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si el estudiante existe
        check_estudiante = supabase.table("estudiante").select("*").eq("id_estudiante", estudiante_id).execute()
        
        if not check_estudiante.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {estudiante_id} no encontrado"
            )
        
        # Verificar si la discapacidad existe
        check_discapacidad = supabase.table("discapacidad_condicion").select("*").eq("id_discapacidad", discapacidad_data.id_discapacidad).execute()
        
        if not check_discapacidad.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Discapacidad con ID {discapacidad_data.id_discapacidad} no encontrada"
            )
        
        # Verificar si ya existe la asociación
        check_asociacion = supabase.table("estudiante_discapacidad").select("*").eq("id_estudiante", estudiante_id).eq("id_discapacidad", discapacidad_data.id_discapacidad).execute()
        
        if check_asociacion.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estudiante ya tiene asociada esta discapacidad"
            )
        
        # Crear la asociación
        data_to_insert = discapacidad_data.model_dump()
        data_to_insert["id_estudiante"] = estudiante_id  # Asegurar que el id_estudiante sea el correcto
        
        response = supabase.table("estudiante_discapacidad").insert(data_to_insert).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al asociar discapacidad al estudiante"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asociar discapacidad: {str(e)}"
        )

@router.put("/{estudiante_id}/discapacidades/{discapacidad_id}", response_model=EstudianteDiscapacidad)
async def update_discapacidad_estudiante(
    estudiante_id: int,
    discapacidad_id: int,
    discapacidad_data: EstudianteDiscapacidadUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza la información de una discapacidad asociada a un estudiante.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si existe la asociación
        check_asociacion = supabase.table("estudiante_discapacidad").select("*").eq("id_estudiante", estudiante_id).eq("id_discapacidad", discapacidad_id).execute()
        
        if not check_asociacion.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la asociación entre el estudiante {estudiante_id} y la discapacidad {discapacidad_id}"
            )
        
        # Filtrar campos nulos para no sobrescribir con None
        update_data = {k: v for k, v in discapacidad_data.model_dump().items() if v is not None}
        
        # Actualizar la asociación
        response = supabase.table("estudiante_discapacidad").update(update_data).eq("id_estudiante", estudiante_id).eq("id_discapacidad", discapacidad_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la información de discapacidad"
            )
            
        return response.data[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar información de discapacidad: {str(e)}"
        )

@router.delete("/{estudiante_id}/discapacidades/{discapacidad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_discapacidad_estudiante(
    estudiante_id: int,
    discapacidad_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Elimina la asociación de una discapacidad a un estudiante.
    """
    supabase = get_supabase_client()
    
    try:
        # Verificar si existe la asociación
        check_asociacion = supabase.table("estudiante_discapacidad").select("*").eq("id_estudiante", estudiante_id).eq("id_discapacidad", discapacidad_id).execute()
        
        if not check_asociacion.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la asociación entre el estudiante {estudiante_id} y la discapacidad {discapacidad_id}"
            )
        
        # Eliminar la asociación
        supabase.table("estudiante_discapacidad").delete().eq("id_estudiante", estudiante_id).eq("id_discapacidad", discapacidad_id).execute()
        
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar asociación de discapacidad: {str(e)}"
        )

# Endpoint para importación de datos desde planilla FUD
@router.post("/importar/fud", response_model=ImportacionResultado)
async def importar_estudiantes_fud(
    estudiantes: List[EstudianteFUD],
    current_user: dict = Depends(get_current_user)
):
    """
    Importa estudiantes desde la planilla FUD.
    """
    supabase = get_supabase_client()
    resultado = ImportacionResultado(total_procesados=len(estudiantes), creados=0, actualizados=0)
    
    try:
        for estudiante_fud in estudiantes:
            try:
                # Verificar si el estudiante ya existe
                check_response = supabase.table("estudiante").select("*").eq("rut", estudiante_fud.rut).execute()
                
                estudiante_dict = {
                    "rut": estudiante_fud.rut,
                    "nombres": estudiante_fud.nombres,
                    "apellido_paterno": estudiante_fud.apellido_paterno,
                    "apellido_materno": estudiante_fud.apellido_materno,
                    "fecha_nacimiento": estudiante_fud.fecha_nacimiento.isoformat(),
                    "genero": estudiante_fud.genero,
                    "email": estudiante_fud.email,
                    "telefono": estudiante_fud.telefono,
                    "semestre_actual": estudiante_fud.semestre
                }
                
                # Si se proporciona una carrera (nombre), buscar su ID
                if estudiante_fud.carrera:
                    carrera_response = supabase.table("programa_estudio").select("id_carrera").eq("nombre_carrera", estudiante_fud.carrera).execute()
                    if carrera_response.data:
                        estudiante_dict["id_carrera"] = carrera_response.data[0]["id_carrera"]
                
                if check_response.data:
                    # Actualizar estudiante existente
                    estudiante_id = check_response.data[0]["id_estudiante"]
                    supabase.table("estudiante").update(estudiante_dict).eq("id_estudiante", estudiante_id).execute()
                    resultado.actualizados += 1
                else:
                    # Crear nuevo estudiante
                    new_estudiante = supabase.table("estudiante").insert(estudiante_dict).execute()
                    estudiante_id = new_estudiante.data[0]["id_estudiante"]
                    resultado.creados += 1
                
                # Si se proporciona una discapacidad, asociarla al estudiante
                if estudiante_fud.discapacidad:
                    # Buscar la discapacidad por nombre
                    disc_response = supabase.table("discapacidad_condicion").select("id_discapacidad").eq("nombre", estudiante_fud.discapacidad).execute()
                    
                    if disc_response.data:
                        disc_id = disc_response.data[0]["id_discapacidad"]
                        
                        # Verificar si ya existe la asociación
                        check_asoc = supabase.table("estudiante_discapacidad").select("*").eq("id_estudiante", estudiante_id).eq("id_discapacidad", disc_id).execute()
                        
                        if not check_asoc.data:
                            # Crear la asociación
                            disc_data = {
                                "id_estudiante": estudiante_id,
                                "id_discapacidad": disc_id,
                                "observaciones": estudiante_fud.observaciones
                            }
                            supabase.table("estudiante_discapacidad").insert(disc_data).execute()
            
            except Exception as e:
                # Registrar error pero continuar con el siguiente estudiante
                resultado.errores.append({
                    "rut": estudiante_fud.rut,
                    "error": str(e)
                })
        
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la importación de estudiantes: {str(e)}"
        )

@router.post("/importar/excel", response_model=ImportacionResultado)
async def importar_excel_fud(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Importa estudiantes desde un archivo Excel (planilla FUD).
    """
    try:
        # Verificar que sea un archivo Excel
        if not file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe ser un Excel (.xls o .xlsx)"
            )
        
        # Leer el contenido del archivo
        contents = await file.read()
        
        # Procesar la planilla FUD
        try:
            estudiantes = procesar_planilla_fud(contents)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al procesar el archivo Excel: {str(e)}"
            )
        
        # Importar los estudiantes
        resultado = await importar_estudiantes_fud(estudiantes, current_user)
        
        return resultado
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la importación del archivo: {str(e)}"
        )

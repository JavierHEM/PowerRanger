import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import io

from app.schemas.estudiante import EstudianteFUD

def parse_date(date_str: str) -> Optional[datetime.date]:
    """Convierte una cadena de fecha en un objeto date"""
    if not date_str or pd.isna(date_str):
        return None
    
    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str).strip(), fmt).date()
        except ValueError:
            continue
    
    return None

def procesar_planilla_fud(file_content: bytes) -> List[EstudianteFUD]:
    """
    Procesa un archivo Excel de planilla FUD y retorna una lista de estudiantes
    """
    # Leer el archivo Excel
    df = pd.read_excel(io.BytesIO(file_content))
    
    # Normalizar nombres de columnas (convertir a minúsculas y reemplazar espacios)
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Mapeo de columnas esperadas en la planilla FUD
    column_mapping = {
        'rut': 'rut',
        'nombres': 'nombres',
        'apellido_paterno': 'apellido_paterno',
        'apellido_materno': 'apellido_materno',
        'fecha_nacimiento': 'fecha_nacimiento',
        'genero': 'genero',
        'email': 'email',
        'telefono': 'telefono',
        'carrera': 'carrera',
        'semestre': 'semestre',
        'discapacidad': 'discapacidad',
        'observaciones': 'observaciones'
    }
    
    # Verificar columnas requeridas
    required_columns = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno']
    for col in required_columns:
        if col not in df.columns and column_mapping.get(col) not in df.columns:
            raise ValueError(f"Columna requerida '{col}' no encontrada en la planilla")
    
    # Procesar cada fila y convertirla en un objeto EstudianteFUD
    estudiantes = []
    for _, row in df.iterrows():
        # Extraer datos usando el mapeo de columnas
        estudiante_data = {}
        for schema_col, excel_col in column_mapping.items():
            if excel_col in df.columns:
                estudiante_data[schema_col] = row[excel_col]
            elif schema_col in df.columns:
                estudiante_data[schema_col] = row[schema_col]
            else:
                estudiante_data[schema_col] = None
        
        # Procesar la fecha de nacimiento
        if 'fecha_nacimiento' in estudiante_data and estudiante_data['fecha_nacimiento']:
            fecha = parse_date(estudiante_data['fecha_nacimiento'])
            if fecha:
                estudiante_data['fecha_nacimiento'] = fecha
        
        # Crear objeto EstudianteFUD si tiene los datos mínimos
        if (estudiante_data.get('rut') and 
            estudiante_data.get('nombres') and 
            estudiante_data.get('apellido_paterno') and
            estudiante_data.get('apellido_materno') and
            estudiante_data.get('fecha_nacimiento')):
            
            # Limpiar valores NaN
            for key, value in estudiante_data.items():
                if pd.isna(value):
                    estudiante_data[key] = None
            
            try:
                estudiante = EstudianteFUD(**estudiante_data)
                estudiantes.append(estudiante)
            except Exception as e:
                print(f"Error al procesar estudiante {estudiante_data.get('rut')}: {str(e)}")
    
    return estudiantes

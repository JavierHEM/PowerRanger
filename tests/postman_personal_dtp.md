# Pruebas del Módulo Personal DTP con Postman

Este documento proporciona instrucciones para probar el módulo CRUD de Personal DTP utilizando Postman.

## Configuración Previa

1. Asegúrate de que el servidor esté en ejecución: `uvicorn app.main:app --reload`
2. Obtén un token de autenticación válido mediante el endpoint de login

## Endpoints Disponibles

### 1. Obtener todos los miembros del personal

- **Método**: GET
- **URL**: `http://localhost:8000/api/v1/personal/`
- **Headers**:
  - Authorization: Bearer {token}
- **Parámetros Query (opcionales)**:
  - skip: número de registros a omitir (default: 0)
  - limit: número máximo de registros a devolver (default: 100)
  - activo: filtrar por estado activo (true/false)

### 2. Obtener un miembro del personal por ID

- **Método**: GET
- **URL**: `http://localhost:8000/api/v1/personal/{personal_id}`
- **Headers**:
  - Authorization: Bearer {token}

### 3. Crear un nuevo miembro del personal

- **Método**: POST
- **URL**: `http://localhost:8000/api/v1/personal/`
- **Headers**:
  - Authorization: Bearer {token}
  - Content-Type: application/json
- **Body**:
  ```json
  {
    "rut": "12345678-9",
    "nombres": "Juan",
    "apellidos": "Pérez",
    "email": "juan.perez@inacap.cl",
    "cargo": "Coordinador DTP",
    "activo": true
  }
  ```

### 4. Actualizar un miembro del personal

- **Método**: PUT
- **URL**: `http://localhost:8000/api/v1/personal/{personal_id}`
- **Headers**:
  - Authorization: Bearer {token}
  - Content-Type: application/json
- **Body** (solo incluir campos a actualizar):
  ```json
  {
    "cargo": "Director DTP",
    "email": "juan.perez.nuevo@inacap.cl"
  }
  ```

### 5. Eliminar (desactivar) un miembro del personal

- **Método**: DELETE
- **URL**: `http://localhost:8000/api/v1/personal/{personal_id}`
- **Headers**:
  - Authorization: Bearer {token}

### 6. Buscar un miembro del personal por RUT

- **Método**: GET
- **URL**: `http://localhost:8000/api/v1/personal/buscar/rut/{rut}`
- **Headers**:
  - Authorization: Bearer {token}

## Ejemplos de Respuestas

### Obtener todos los miembros del personal (Éxito)
```json
[
  {
    "id_personal": 1,
    "rut": "12345678-9",
    "nombres": "Juan",
    "apellidos": "Pérez",
    "email": "juan.perez@inacap.cl",
    "cargo": "Coordinador DTP",
    "activo": true
  },
  {
    "id_personal": 2,
    "rut": "98765432-1",
    "nombres": "María",
    "apellidos": "González",
    "email": "maria.gonzalez@inacap.cl",
    "cargo": "Psicóloga DTP",
    "activo": true
  }
]
```

### Crear un nuevo miembro del personal (Éxito)
```json
{
  "id_personal": 3,
  "rut": "11223344-5",
  "nombres": "Carlos",
  "apellidos": "Rodríguez",
  "email": "carlos.rodriguez@inacap.cl",
  "cargo": "Asistente DTP",
  "activo": true
}
```

### Error: Personal no encontrado
```json
{
  "detail": "Personal con ID 999 no encontrado"
}
```

### Error: RUT duplicado
```json
{
  "detail": "Ya existe un personal con el RUT 12345678-9"
}
```

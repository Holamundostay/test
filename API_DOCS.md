# 📚 Documentación de API - Inventario CEYE

## Base URL
```
http://localhost:8000
```

## Documentación Interactiva
Mientras el servidor está corriendo, abre:
```
http://localhost:8000/docs
```

---

## 📋 Tabla de Contenidos

1. [Items (Artículos)](#items)
2. [Users (Usuarios)](#users)
3. [Counts (Conteos)](#counts)
4. [Audit Logs (Auditoría)](#audit-logs)
5. [Health (Verificación)](#health)

---

## <a name="items"></a> 📦 Items (Artículos)

### GET /items
**Obtener todos los artículos del inventario**

```bash
curl -X GET http://localhost:8000/items
```

**Respuesta (200 OK)**:
```json
[
  {
    "id": 1,
    "name": "Guantes quirúrgicos",
    "description": "Guantes estériles tamaño M",
    "quantity": 50.0,
    "category": "Materiales desechables",
    "location": "Quirófano Ceye",
    "last_updated": "2026-04-24T10:30:00",
    "updated_by": "María García"
  },
  ...
]
```

---

### POST /items
**Crear un nuevo artículo**

```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bisturí",
    "description": "Bisturí desechable #10",
    "quantity": 20,
    "category": "Instrumentos quirúrgicos",
    "location": "Quirófano Ceye",
    "updated_by": "María García"
  }'
```

**Parámetros Requeridos**:
- `name` (string): Nombre del artículo
- `quantity` (number): Cantidad inicial
- `category` (string): Categoría

**Parámetros Opcionales**:
- `description` (string): Descripción
- `location` (string): Ubicación (default: "Quirófano Ceye")
- `updated_by` (string): Usuario (default: "Sistema")

**Respuesta (200 OK)**:
```json
{
  "id": 2,
  "name": "Bisturí",
  "description": "Bisturí desechable #10",
  "quantity": 20.0,
  "category": "Instrumentos quirúrgicos",
  "location": "Quirófano Ceye",
  "last_updated": "2026-04-24T10:35:00",
  "updated_by": "María García"
}
```

---

### PUT /items/{item_id}
**Actualizar cantidad de un artículo**

```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 45,
    "updated_by": "Carlos López"
  }'
```

**Parámetros**:
- `item_id` (integer): ID del artículo
- `quantity` (number): Nueva cantidad
- `updated_by` (string): Usuario que realiza el cambio

**Respuesta (200 OK)**:
```json
{
  "id": 1,
  "name": "Guantes quirúrgicos",
  "description": "Guantes estériles tamaño M",
  "quantity": 45.0,
  "category": "Materiales desechables",
  "location": "Quirófano Ceye",
  "last_updated": "2026-04-24T10:40:00",
  "updated_by": "Carlos López"
}
```

---

### DELETE /items/{item_id}
**Eliminar un artículo del inventario**

```bash
curl -X DELETE http://localhost:8000/items/1
```

**Parámetros**:
- `item_id` (integer): ID del artículo a eliminar

**Respuesta (200 OK)**:
```json
{
  "message": "Item deleted"
}
```

---

## <a name="users"></a> 👥 Users (Usuarios)

### GET /users
**Obtener todos los usuarios activos**

```bash
curl -X GET http://localhost:8000/users
```

**Respuesta (200 OK)**:
```json
[
  {
    "id": 1,
    "username": "maria",
    "full_name": "María García",
    "role": "enfermera",
    "created_at": "2026-04-24T00:00:00",
    "is_active": 1
  },
  ...
]
```

---

### POST /users
**Crear un nuevo usuario**

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "full_name": "Juan Pérez",
    "role": "enfermera"
  }'
```

**Parámetros Requeridos**:
- `username` (string): Usuario único
- `full_name` (string): Nombre completo

**Parámetros Opcionales**:
- `role` (string): Rol (default: "enfermera")
  - `enfermera`: Enfermera estándar
  - `supervisor`: Supervisor
  - `admin`: Administrador

**Respuesta (200 OK)**:
```json
{
  "id": 5,
  "username": "juan",
  "full_name": "Juan Pérez",
  "role": "enfermera",
  "created_at": "2026-04-24T10:45:00",
  "is_active": 1
}
```

---

### GET /users/{user_id}
**Obtener un usuario específico**

```bash
curl -X GET http://localhost:8000/users/1
```

**Parámetros**:
- `user_id` (integer): ID del usuario

**Respuesta (200 OK)**:
```json
{
  "id": 1,
  "username": "maria",
  "full_name": "María García",
  "role": "enfermera",
  "created_at": "2026-04-24T00:00:00",
  "is_active": 1
}
```

---

## <a name="counts"></a> 📋 Counts (Conteos)

### POST /counts
**Registrar un conteo de inventario**

```bash
curl -X POST http://localhost:8000/counts \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "user_id": 1,
    "quantity_on_hand": 48,
    "expected_quantity": 50,
    "notes": "Dos pares dañados"
  }'
```

**Parámetros Requeridos**:
- `item_id` (integer): ID del artículo contado
- `user_id` (integer): ID del usuario que realiza el conteo
- `quantity_on_hand` (number): Cantidad encontrada
- `expected_quantity` (number): Cantidad esperada

**Parámetros Opcionales**:
- `notes` (string): Notas del conteo

**Respuesta (200 OK)**:
```json
{
  "id": 1,
  "item_id": 1,
  "user_id": 1,
  "quantity_on_hand": 48.0,
  "expected_quantity": 50.0,
  "discrepancy": -2.0,
  "count_date": "2026-04-24T10:50:00",
  "notes": "Dos pares dañados",
  "item": {
    "id": 1,
    "name": "Guantes quirúrgicos",
    ...
  },
  "user": {
    "id": 1,
    "username": "maria",
    "full_name": "María García",
    ...
  }
}
```

---

### GET /counts
**Obtener todos los conteos**

```bash
curl -X GET http://localhost:8000/counts
```

**Parámetros Opcionales (Query)**:
- `item_id` (integer): Filtrar por artículo
- `user_id` (integer): Filtrar por usuario

```bash
# Ejemplo: obtener conteos de María
curl -X GET "http://localhost:8000/counts?user_id=1"
```

**Respuesta (200 OK)**:
```json
[
  {
    "id": 1,
    "item_id": 1,
    "user_id": 1,
    "quantity_on_hand": 48.0,
    "expected_quantity": 50.0,
    "discrepancy": -2.0,
    "count_date": "2026-04-24T10:50:00",
    "notes": "Dos pares dañados",
    ...
  },
  ...
]
```

---

### GET /items/{item_id}/counts
**Obtener conteos de un artículo específico**

```bash
curl -X GET http://localhost:8000/items/1/counts
```

**Parámetros**:
- `item_id` (integer): ID del artículo

**Respuesta (200 OK)**:
```json
[
  {
    "id": 1,
    "item_id": 1,
    "quantity_on_hand": 48.0,
    ...
  },
  {
    "id": 2,
    "item_id": 1,
    "quantity_on_hand": 47.0,
    ...
  }
]
```

---

## <a name="audit-logs"></a> 🔍 Audit Logs (Auditoría)

### GET /audit-logs
**Obtener registros de auditoría**

```bash
curl -X GET http://localhost:8000/audit-logs
```

**Parámetros Opcionales (Query)**:
- `item_id` (integer): Filtrar por artículo
- `user_id` (integer): Filtrar por usuario
- `action` (string): Filtrar por tipo de acción
  - `created`: Artículo creado
  - `updated`: Cantidad actualizada
  - `counted`: Conteo realizado
  - `deleted`: Artículo eliminado

```bash
# Ejemplo: ver cambios de María
curl -X GET "http://localhost:8000/audit-logs?user_id=1"

# Ejemplo: ver solo creaciones
curl -X GET "http://localhost:8000/audit-logs?action=created"
```

**Respuesta (200 OK)**:
```json
[
  {
    "id": 1,
    "item_id": 1,
    "user_id": 1,
    "action": "updated",
    "old_quantity": 50.0,
    "new_quantity": 48.0,
    "action_date": "2026-04-24T10:50:00",
    "notes": "Quantity updated from 50 to 48",
    "item": {
      "id": 1,
      "name": "Guantes quirúrgicos",
      ...
    },
    "user": {
      "id": 1,
      "username": "maria",
      "full_name": "María García",
      ...
    }
  },
  ...
]
```

---

### GET /items/{item_id}/audit-logs
**Obtener historial de auditoría de un artículo**

```bash
curl -X GET http://localhost:8000/items/1/audit-logs
```

**Parámetros**:
- `item_id` (integer): ID del artículo

**Respuesta (200 OK)**:
```json
[
  {
    "id": 1,
    "item_id": 1,
    "action": "created",
    "new_quantity": 50.0,
    "action_date": "2026-04-20T00:00:00",
    ...
  },
  {
    "id": 2,
    "item_id": 1,
    "action": "updated",
    "old_quantity": 50.0,
    "new_quantity": 48.0,
    "action_date": "2026-04-24T10:50:00",
    ...
  }
]
```

---

## <a name="health"></a> ❤️ Health (Verificación)

### GET /health
**Verificar si el servidor está funcionando**

```bash
curl -X GET http://localhost:8000/health
```

**Respuesta (200 OK)**:
```json
{
  "status": "ok"
}
```

---

## 🔐 Códigos de Error

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| **200 OK** | Solicitud exitosa | Datos obtenidos/creados correctamente |
| **201 Created** | Recurso creado | Nuevo artículo creado |
| **400 Bad Request** | Datos inválidos | Cantidad negativa |
| **404 Not Found** | Recurso no existe | ID de artículo inexistente |
| **422 Unprocessable Entity** | Error de validación | Campos requeridos faltantes |
| **500 Server Error** | Error del servidor | Problema en la base de datos |

---

## 📊 Categorías Válidas

```json
[
  "Instrumentos quirúrgicos",
  "Medicamentos",
  "Materiales desechables",
  "Equipo médico",
  "Otros"
]
```

---

## 🔄 Flujo de Datos Típico

### Día Típico:

1. **Mañana**: Obtener items y realizar conteos
```
GET /items
→ POST /counts (para cada artículo)
→ GET /items/{item_id}/counts (ver histórico)
```

2. **Tarde**: Supervisar cambios
```
GET /audit-logs?user_id=1
→ Identificar cambios
```

3. **Noche**: Preparar reporte
```
GET /counts
→ GET /audit-logs
→ Generar análisis
```

---

## 💡 Ejemplos de Casos de Uso

### Caso 1: Conteo Diario Completo

```bash
# 1. Obtener todos los artículos
curl -X GET http://localhost:8000/items

# 2. Para cada artículo, registrar conteo
curl -X POST http://localhost:8000/counts \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "user_id": 1,
    "quantity_on_hand": 48,
    "expected_quantity": 50,
    "notes": "Discrepancia encontrada"
  }'

# 3. Ver conteos de hoy
curl -X GET http://localhost:8000/counts?user_id=1
```

### Caso 2: Investigar Discrepancia

```bash
# 1. Ver todos los conteos del artículo
curl -X GET http://localhost:8000/items/1/counts

# 2. Ver historial completo del artículo
curl -X GET http://localhost:8000/items/1/audit-logs

# 3. Ver cambios de un usuario específico
curl -X GET "http://localhost:8000/audit-logs?user_id=1&item_id=1"
```

### Caso 3: Agregar Nuevo Material

```bash
# 1. Crear artículo
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendaje estéril",
    "description": "Vendaje 10x10cm",
    "quantity": 100,
    "category": "Materiales desechables",
    "updated_by": "María García"
  }'

# 2. Registrar conteo inicial
curl -X POST http://localhost:8000/counts \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 6,
    "user_id": 1,
    "quantity_on_hand": 100,
    "expected_quantity": 100,
    "notes": "Conteo inicial - material nuevo"
  }'
```

---

## 🔧 Testing con cURL

Instala cURL y prueba:

```bash
# Test básico
curl -X GET http://localhost:8000/health

# Ver documentación interactiva
open http://localhost:8000/docs

# Con datos JSON
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "name": "Test Item",
  "quantity": 10,
  "category": "Otros",
  "updated_by": "Test"
}
EOF
```

---

## 📝 Notas Importantes

- La **discrepancia** se calcula automáticamente: `quantity_on_hand - expected_quantity`
- Todos los cambios crean registros de auditoría automáticamente
- Los usuarios se registran automáticamente en cada operación
- La base de datos se crea automáticamente en `backend/inventory.db`
- Los timestamps están en UTC (GMT+0)

---

**Última actualización**: Abril 2026  
**Versión API**: 1.0

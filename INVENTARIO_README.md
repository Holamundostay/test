# Sistema de Inventario - Quirófano CEYE

## 📋 Descripción General

Aplicación web completa para gestionar el inventario de materiales quirúrgicos en el departamento CEYE Quirófano. Permite:

✅ **Gestión de inventario**: Agregar, modificar y eliminar materiales  
✅ **Conteo de piezas**: Realizar conteos regulares y conocer las diferencias  
✅ **Auditoría completa**: Registro de todos los cambios y quién los realizó  
✅ **Reportes**: Visualizar histórico de conteos y cambios  
✅ **Control de usuarios**: Cada acción es rastreable por usuario  

---

## 🏗️ Arquitectura

```
Frontend (Vue 3)
    ↓
API REST (FastAPI)
    ↓
Base de Datos (SQLite)
```

### Backend
- **Framework**: FastAPI
- **Base de datos**: SQLite
- **ORM**: SQLAlchemy
- **Validación**: Pydantic

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Cliente HTTP**: Axios
- **Estilos**: CSS moderno con gradientes

---

## 📦 Instalación y Configuración

### 1. **Requisitos Previos**
```bash
- Python 3.10+
- Node.js 16+ (para frontend)
- npm o yarn
```

### 2. **Instalar Dependencias Backend**

```bash
cd backend
pip install -r requirements.txt
```

### 3. **Instalar Dependencias Frontend**

```bash
cd frontend
npm install
```

---

## 🚀 Cómo Ejecutar

### Opción 1: Ejecutar con Docker (Recomendado)

```bash
docker-compose up -d
```

Accede a:
- Frontend: http://localhost:5173
- API: http://localhost:8000/docs

### Opción 2: Ejecutar Localmente

**Terminal 1 - Backend**:
```bash
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

La aplicación estará en: http://localhost:5173

---

## 📊 Estructura de Datos

### Tablas de la Base de Datos

#### **1. Usuarios (users)**
```
- id: Identificador único
- username: Usuario (ej: maria)
- full_name: Nombre completo
- role: Rol (enfermera, supervisor, admin)
- created_at: Fecha de creación
- is_active: Estado (1=activo, 0=inactivo)
```

#### **2. Artículos (items)**
```
- id: Identificador único
- name: Nombre del artículo
- description: Descripción
- quantity: Cantidad actual
- category: Categoría
- location: Ubicación (Quirófano Ceye)
- last_updated: Última actualización
- updated_by: Quién lo actualizó
```

#### **3. Conteos (counts)**
```
- id: Identificador único
- item_id: Referencia al artículo
- user_id: Quién realizó el conteo
- quantity_on_hand: Cantidad encontrada
- expected_quantity: Cantidad esperada
- discrepancy: Diferencia (encontrada - esperada)
- count_date: Fecha del conteo
- notes: Notas del conteo
```

#### **4. Auditoría (audit_logs)**
```
- id: Identificador único
- item_id: Artículo afectado
- user_id: Usuario que realizó el cambio
- action: Tipo de acción (created, updated, counted, deleted)
- old_quantity: Cantidad anterior
- new_quantity: Cantidad nueva
- action_date: Fecha del cambio
- notes: Notas adicionales
```

---

## 🔑 Características Principales

### 1. **Autenticación de Usuarios**
Al iniciar, selecciona tu usuario. Los usuarios predeterminados incluyen:
- **María García** (Enfermera)
- **Carlos López** (Enfermera)
- **Ana Martínez** (Supervisor)
- **Administrador** (Admin)

### 2. **Gestión de Inventario**

#### Agregar Artículo
1. Ve a pestaña "➕ Agregar artículo"
2. Completa nombre, descripción, cantidad y categoría
3. Click en "Agregar Artículo"

#### Ajustar Cantidad
1. En "📦 Inventario", busca el artículo
2. Click en "✏️ Ajustar cantidad"
3. Ingresa la nueva cantidad
4. Confirma el cambio

### 3. **Realizar Conteos**

#### Procedimiento
1. Ve a pestaña "📋 Realizar conteo"
2. Selecciona el artículo a contar
3. Ingresa la cantidad encontrada
4. Agrega notas si es necesario (ej: "Falta buscar en estante C")
5. Click en "Registrar Conteo"

**Importante**: La aplicación muestra automáticamente la diferencia:
- ✅ Verde (+): Hay MÁS del esperado
- ❌ Rojo (-): Faltan piezas del stock
- ➖ Gris (0): Coincide el conteo

### 4. **Ver Reportes**

#### Conteos Recientes
- Tabla con todos los conteos realizados
- Filtrar por artículo o usuario
- Ve las discrepancias claramente

#### Auditoría de Cambios
- Historial completo de todo lo que cambió
- Quién hizo cada cambio y cuándo
- Código de colores por tipo de acción

---

## 📱 Interfaz de Usuario

### Pantalla de Login
- Selecciona tu usuario con un clic
- Interfaz intuitiva con avatares

### Pestañas Principales
1. **📦 Inventario**: Vista general de todos los materiales
2. **➕ Agregar artículo**: Formulario para nuevos materiales
3. **📋 Realizar conteo**: Interfaz para contar piezas
4. **📊 Reportes**: Histórico y auditoría

### Filtros y Búsqueda
- Busca por nombre de artículo
- Filtra por categoría
- Filtra reportes por usuario

---

## 🔐 Seguridad y Auditoría

Todos los cambios en el inventario quedan registrados:
- ✓ Quién realizó el cambio
- ✓ Cuándo se realizó
- ✓ Qué cambió (antes y después)
- ✓ Por qué (notas adicionales)

---

## 📊 Categorías de Materiales

- Instrumentos quirúrgicos
- Medicamentos
- Materiales desechables
- Equipo médico
- Otros

---

## 🆘 Solución de Problemas

### El frontend no conecta con el backend
```
✓ Verifica que el backend esté corriendo en http://localhost:8000
✓ Verifica CORS: El backend permite conexiones del frontend
✓ Mira la consola del navegador (F12) para ver el error
```

### La base de datos no se crea
```
✓ Verifica que SQLite esté instalado
✓ Verifica permisos de lectura/escritura en la carpeta
✓ Elimina inventory.db y déjalo regenerar
```

### No aparecen los usuarios
```
✓ Reinicia el servidor backend
✓ Verifica que create_sample_data() se ejecutó correctamente
✓ Abre la BD con SQLite Browser y verifica la tabla users
```

---

## 📈 Casos de Uso

### Caso 1: Conteo Inicial de Turno
1. Inicia sesión como tu usuario
2. Ve a "Realizar conteo"
3. Cuenta cada material
4. Registra los conteos con notas si hay diferencias
5. El sistema identifica automáticamente faltantes

### Caso 2: Agregar Nuevo Material
1. Ve a "Agregar artículo"
2. Completa todos los datos
3. Define una cantidad inicial (ej: basado en recepción)
4. El sistema empieza a rastrear este material

### Caso 3: Reporte de Faltantes
1. Ve a "Reportes" → "Conteos Recientes"
2. Busca por usuario o artículo
3. Las filas rojas muestran faltantes
4. Exporta para reportar a dirección

### Caso 4: Auditoría de Cambios
1. Ve a "Reportes" → "Auditoría de Cambios"
2. Ve quién hizo qué y cuándo
3. Identifica patrones o problemas
4. Usa para investigaciones

---

## 🔄 Flujos de Trabajo

### Workflow Diario
```
Mañana (Inicio)
  ↓
Conteo inicial de todos los materiales
  ↓
Registrar diferencias (si las hay)
  ↓
Realizar ajustes basados en consumo
  ↓
Tarde (Supervisor)
  ↓
Revisar conteos de la mañana
  ↓
Noche (Preparación)
  ↓
Conteo final y preparación para próximo día
```

---

## 🎨 Características Visuales

- ✨ Interfaz moderna con gradientes
- 📱 Responsive: funciona en desktop y tablet
- 🎯 Iconos intuitivos en cada sección
- 🎨 Código de colores para estados (rojo = falta, verde = sobre, gris = exacto)
- ⚡ Carga rápida y fluida

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Contar Guantes
```
1. Login como María
2. Inventario → Busca "Guantes quirúrgicos"
3. Sistema muestra: "Stock actual: 50"
4. Ve a Realizar conteo → Selecciona Guantes
5. Cuenta físicamente: "Encontré 48"
6. Sistema muestra: Diferencia: -2
7. Agrega nota: "Dos pares dañados, descartados"
8. Registra conteo
```

### Ejemplo 2: Agregar Nuevo Material
```
1. Ve a Agregar artículo
2. Nombre: "Gasas estériles 10x10"
3. Descripción: "Paquete de 50 piezas"
4. Cantidad: 120 (4 paquetes recibidos)
5. Categoría: "Materiales desechables"
6. Click Agregar → Confirmado ✓
```

### Ejemplo 3: Revisar Reportes
```
1. Ve a Reportes
2. Conteos Recientes → Filtra por usuario "María"
3. Ve sus conteos del últimos días
4. Identifica artículos con problemas recurrentes
5. Auditoría → Ve todos los cambios por item
```

---

## 🚀 Próximas Mejoras Sugeridas

- [ ] Exportar reportes a PDF/Excel
- [ ] Gráficos de tendencias
- [ ] Alertas automáticas de bajo stock
- [ ] Código de barras para conteos más rápidos
- [ ] Integración con sistema de pedidos
- [ ] Búsqueda avanzada
- [ ] Roles y permisos granulares
- [ ] Respaldo automático de datos

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisa esta documentación
2. Verifica los logs del servidor
3. Consulta la base de datos directamente con SQLite Browser

---

## 📄 Licencia

Aplicación interna para uso en CEYE Quirófano.

---

**Última actualización**: Abril 2026  
**Versión**: 2.0 con sistema de conteos y auditoría

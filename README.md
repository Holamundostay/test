# Sistema de Control de Inventario - Quirófano Ceye

Una aplicación full-stack para el control de inventario del área de quirófano Ceye, permitiendo al personal de enfermería gestionar el inventario de manera simple y rápida durante sus turnos.

## Características

- **Visualización del inventario**: Vista completa de todos los artículos con cantidades, categorías y última actualización
- **Control por turnos**: Cada turno (Mañana, Tarde, Noche) puede actualizar el inventario
- **Gestión de artículos**: Agregar, modificar cantidades y eliminar artículos
- **Categorización**: Organización por categorías (Instrumentos quirúrgicos, Medicamentos, etc.)
- **Filtrado**: Búsqueda y filtrado por categoría
- **Historial**: Registro de quién y cuándo se actualizó cada artículo

## Arquitectura del Proyecto

```
test/
├── backend/
│   ├── app.py              # API FastAPI para gestión de inventario
│   ├── requirements.txt     # Dependencias Python
│   └── Dockerfile         # Contenedor backend
├── frontend/
│   ├── src/
│   │   ├── main.js        # Punto de entrada Vue.js
│   │   └── App.vue        # Componente principal de inventario
│   ├── index.html         # Plantilla HTML
│   ├── package.json       # Dependencias Node.js
│   ├── vite.config.js     # Configuración Vite
│   └── Dockerfile         # Contenedor frontend
├── docker-compose.yml     # Orquestación Docker
└── README.md             # Este archivo
```

## Prerrequisitos

- Python 3.8+
- Node.js 16+
- npm o yarn

## Instalación y Ejecución Manual

### Backend

1. Instalar dependencias Python:
```bash
cd backend
pip install -r requirements.txt
```

2. Ejecutar el servidor backend:
```bash
uvicorn app:app --reload
```
El backend estará disponible en http://localhost:8000

### Frontend

1. Instalar dependencias Node.js:
```bash
cd frontend
npm install
```

2. Ejecutar el servidor de desarrollo:
```bash
npm run dev
```
El frontend estará disponible en http://localhost:5173

## Ejecución con Docker Compose

Si tienes Docker instalado:

1. Navegar al directorio del proyecto:
```bash
cd test
```

2. Construir e iniciar los contenedores:
```bash
docker compose up --build
```

La aplicación estará disponible en:
- **Frontend**: http://localhost:5173
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Desarrollo

### Backend
- FastAPI con SQLAlchemy ORM
- Base de datos SQLite para simplicidad
- Endpoints RESTful para CRUD de artículos

### Frontend
- Vue.js 3 con Composition API
- Axios para comunicación con API
- Interfaz responsive y fácil de usar

## Uso

1. **Seleccionar turno**: Elegir el turno actual (Mañana/Tarde/Noche)
2. **Agregar artículos**: Usar el formulario para añadir nuevos artículos al inventario
3. **Actualizar cantidades**: Para cada artículo, usar los controles +/- o ingresar cantidad directamente
4. **Aplicar cambios**: Hacer clic en "Aplicar" para guardar las actualizaciones
5. **Filtrar**: Usar el filtro de categoría para encontrar artículos específicos
6. **Eliminar**: Opción para remover artículos del inventario

## API Endpoints

- `GET /items` - Obtener todos los artículos
- `POST /items` - Crear nuevo artículo
- `PUT /items/{id}` - Actualizar cantidad de artículo
- `DELETE /items/{id}` - Eliminar artículo
- `GET /health` - Verificar estado del servidor
- SQLite database
- Auto-reload on file changes
- Endpoint: `http://localhost:8000`

### Frontend
- Vue 3 with Vite
- Axios for API calls
- Hot Module Replacement (HMR)
- Endpoint: `http://localhost:5173`

## API Endpoints

- `POST /save` - Save a new journal entry
- `GET /entries` - Get all journal entries
- `GET /health` - Health check
- `GET /docs` - Swagger API documentation

## Stopping the Containers

```bash
docker-compose down
```

## Troubleshooting

If you encounter CORS issues, the backend is configured to allow all origins in development mode.

If the frontend can't connect to the backend, ensure both containers are running and check the Docker Compose logs:
```bash
docker-compose logs
```

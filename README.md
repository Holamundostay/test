# Daily Appreciation Journal

A full-stack application for journaling daily appreciations and challenges using Python backend, Vue.js frontend, and SQLite database, all containerized with Docker.

## Project Structure

```
test/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile         # Backend container config
├── frontend/
│   ├── src/
│   │   ├── main.js        # Entry point
│   │   └── App.vue        # Main Vue component
│   ├── index.html         # HTML template
│   ├── package.json       # Node.js dependencies
│   ├── vite.config.js     # Vite configuration
│   └── Dockerfile         # Frontend container config
├── docker-compose.yml     # Docker Compose orchestration
└── README.md             # This file
```

## Prerequisites

- Docker
- Docker Compose

## Running with Docker Compose

1. Navigate to the project root:
```bash
cd test
```

2. Build and start the containers:
```bash
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development

### Backend
- FastAPI with SQLAlchemy ORM
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

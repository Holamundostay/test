# Local Development Setup Guide

## Prerequisites

Before starting, ensure you have these installed:

1. **Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 16+**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

## Setup Instructions

### Option 1: Automated Setup (Windows)

#### Using PowerShell:
```powershell
# Navigate to project root
cd "c:\Users\Administrator\Documents\새 폴더\test"

# Run the setup script
.\setup.ps1
```

#### Using Command Prompt (CMD):
```cmd
cd c:\Users\Administrator\Documents\새 폴더\test
setup.bat
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn app:app --reload
```

Backend will run at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

#### 2. Frontend Setup (in a separate terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend will run at: **http://localhost:5173**

## Accessing the Application

Once both servers are running:

1. Open your browser to: **http://localhost:5173**
2. Use the journal to:
   - Add appreciations and challenges
   - View past entries
   - Data is stored in SQLite (`backend/journal.db`)

## Project Structure

```
test/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── journal.db          # SQLite database (created on first run)
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   └── App.vue
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── node_modules/       # Frontend packages
├── setup.ps1               # PowerShell setup script
├── setup.bat               # Batch setup script
└── README.md
```

## Backend Information

**Stack:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- Uvicorn (ASGI server)

**API Endpoints:**
- `POST /save` - Save a new entry
- `GET /entries` - Get all entries
- `GET /health` - Health check
- `GET /docs` - Swagger documentation

## Frontend Information

**Stack:**
- Vue 3 (JavaScript framework)
- Vite (Build tool)
- Axios (HTTP client)

**Features:**
- Hot Module Replacement (HMR)
- Real-time UI updates
- Responsive design

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Use a different port
python -m uvicorn app:app --reload --port 8001
```

**Database errors:**
```bash
# Delete the database to start fresh
rm backend/journal.db

# Or on Windows
del backend\journal.db
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Vite will automatically use the next available port
npm run dev
```

**Dependencies issues:**
```bash
# Clear npm cache and reinstall
rm -r node_modules package-lock.json
npm install
```

**CORS errors:**
- Backend is configured to allow all origins in development
- Check that backend is running at http://localhost:8000

## Production Build

To build for production:

```bash
# Frontend
cd frontend
npm run build

# Output will be in frontend/dist/
```

## Stopping the Application

- **Backend**: Press `Ctrl+C` in the backend terminal
- **Frontend**: Press `Ctrl+C` in the frontend terminal

## Next Steps

- Start both servers as described above
- Open http://localhost:5173
- Create your first journal entry
- Data persists in `backend/journal.db`

For more information, see README.md

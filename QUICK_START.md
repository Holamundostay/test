# Quick Start Reference

## For Local Development (Recommended for Development)

### Windows - Automated Setup

```powershell
# 1. Run setup
.\setup.ps1

# 2. Run the app
.\start.ps1
```

Or using Command Prompt:
```cmd
setup.bat
start.bat
```

### macOS / Linux

```bash
# 1. Backend setup
cd backend
pip install -r requirements.txt

# 2. Frontend setup (in another terminal)
cd frontend
npm install

# 3. Start backend (from backend folder)
python -m uvicorn app:app --reload

# 4. Start frontend (from frontend folder)
npm run dev
```

### Access the App
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## For Docker Deployment

```bash
docker-compose up --build
```

Then access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in backend |
| `npm not found` | Install Node.js from https://nodejs.org |
| `python not found` | Install Python from https://python.org |
| Port already in use | Check LOCAL_SETUP.md for port alternatives |
| CORS errors | Verify backend is running and available |

---

## Project Structure

```
├── backend/              # FastAPI + SQLite
│   ├── app.py
│   └── requirements.txt
├── frontend/             # Vue 3 + Vite
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml    # Docker deployment
├── setup.ps1 / setup.bat # Automated setup
└── start.ps1 / start.bat # Quick start
```

---

## Development Tips

- **Backend auto-reload**: Changes to Python files automatically restart the server
- **Frontend HMR**: Changes to Vue components instantly reflect in the browser
- **Database**: SQLite file created at `backend/journal.db`
- **API Docs**: Interactive Swagger docs at http://localhost:8000/docs

---

For detailed setup instructions, see `LOCAL_SETUP.md`
For Docker instructions, see `README.md`

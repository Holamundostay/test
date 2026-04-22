# Quick start script for PowerShell - Runs both backend and frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Daily Appreciation Journal" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend dependencies are installed
if (-not (Test-Path "backend\requirements.txt")) {
    Write-Host "Error: Please run setup.ps1 first to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Backend Server (FastAPI)..." -ForegroundColor Yellow
$backendScript = {
    Set-Location backend
    Write-Host "Backend starting at http://localhost:8000" -ForegroundColor Green
    Write-Host "API Docs at http://localhost:8000/docs" -ForegroundColor Green
    python -m uvicorn app:app --reload
}

Write-Host "Starting Frontend Server (Vite)..." -ForegroundColor Yellow
$frontendScript = {
    Set-Location frontend
    Write-Host "Frontend starting at http://localhost:5173" -ForegroundColor Green
    npm run dev
}

# Start both servers in background
Start-Process pwsh -ArgumentList "-NoExit", "-Command", $backendScript -WindowStyle Normal
Start-Sleep -Seconds 2
Start-Process pwsh -ArgumentList "-NoExit", "-Command", $frontendScript -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Servers Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each terminal window to stop the servers" -ForegroundColor Yellow
Write-Host ""

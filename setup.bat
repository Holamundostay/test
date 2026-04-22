@echo off
REM Setup script for Windows - Local Development

echo ========================================
echo Setting up Daily Appreciation Journal
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8+ from python.org
    exit /b 1
)

REM Check Node.js
echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo Node.js is not installed. Please install from nodejs.org
    exit /b 1
)

echo.
echo ========================================
echo Installing Backend Dependencies
echo ========================================
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install backend dependencies
    exit /b 1
)
cd ..

echo.
echo ========================================
echo Installing Frontend Dependencies
echo ========================================
cd frontend
npm install
if errorlevel 1 (
    echo Failed to install frontend dependencies
    exit /b 1
)
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo 1. Open a terminal in the backend folder and run:
echo    python -m uvicorn app:app --reload
echo.
echo 2. Open another terminal in the frontend folder and run:
echo    npm run dev
echo.
echo Then visit: http://localhost:5173
echo.

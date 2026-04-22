@echo off
REM ¡Este es un archivo especial que ayuda a iniciar nuestra app de Diario de Gratitud!
REM Piénsalo como un robot ayudante que:
REM 1. Inicia el "motor" (backend - la parte que guarda la información)
REM 2. Inicia la "pantalla" (frontend - la parte que ves y usas)
REM @echo off significa "no me muestres los comandos, solo muestra los resultados"

REM ¡Vamos a mostrar un mensaje de bienvenida cool!
echo ========================================
echo Iniciando Diario de Gratitud Diario
echo ========================================
echo.

REM Antes de empezar, necesitamos verificar: "¿Alguien ya preparó las herramientas que necesitamos?"
REM (Esto verifica si setup.bat ya se ha ejecutado)
if not exist "backend\requirements.txt" (
    echo Error: Por favor ejecuta setup.bat primero para instalar las dependencias
    exit /b 1
)

REM Mensaje: Estamos a punto de iniciar el backend (el "cerebro pensante" de nuestra app)
echo Iniciando Servidor Backend (FastAPI)...
REM Inicia una NUEVA ventana llamada "Backend - FastAPI"
REM cd backend = entra en la carpeta backend
REM python -m uvicorn... = inicia el servidor que escucha las solicitudes
REM --reload = reinicia automáticamente cuando hacemos cambios (¡como magia!)
start "Backend - FastAPI" cmd /k "cd backend && python -m uvicorn app:app --reload"

REM Espera 3 segundos para que el backend tenga tiempo de despertar
timeout /t 3 /nobreak

REM Mensaje: Ahora estamos a punto de iniciar el frontend (la "cara bonita" de nuestra app)
echo Iniciando Servidor Frontend (Vite)...
REM Inicia una NUEVA ventana para el frontend
REM cd frontend = entra en la carpeta frontend
REM npm run dev = inicia el servidor de visualización del sitio web
start "Frontend - Vite" cmd /k "cd frontend && npm run dev"

REM ¡Ahora mostremos dónde encontrar nuestra app!
echo.
echo ========================================
echo ¡Servidores Iniciados!
echo ========================================
echo.
REM Estas son las direcciones (como direcciones de casa) donde puedes visitar cada servidor:
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
REM Esta es una página especial con documentación sobre cómo funciona el backend:
echo Documentación de API: http://localhost:8000/docs
echo.
REM Instrucciones finales para el usuario
echo Presiona Ctrl+C en cada ventana de terminal para detener los servidores
echo.

@echo off
setlocal enabledelayedexpansion

REM Add Node.js to PATH for this session
set PATH=C:\Program Files\nodejs;%PATH%

REM Navigate to frontend
cd /d "c:\Users\Administrator\Documents\새 폴더\test\frontend"

REM Clean up old files
if exist node_modules rmdir /s /q node_modules 2>nul
if exist package-lock.json del package-lock.json 2>nul

REM Run npm install
npm install

REM Run npm dev
npm run dev

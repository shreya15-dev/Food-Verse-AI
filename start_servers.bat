@echo off
title Food Verse AI - Launcher
echo ========================================================
echo               FOOD VERSE AI - FULL-STACK
echo    "Smarter Food Choices. Safer Kitchens. Healthier Living."
echo ========================================================
echo.

echo [1/2] Launching Python Flask Backend API (Port 5000)...
start "Food Verse AI - Backend API" cmd /k "cd /d %~dp0backend && python app.py"

echo [2/2] Launching React + Vite Frontend (Port 5173)...
start "Food Verse AI - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are starting!
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo.
echo Opening browser in 3 seconds...
timeout /t 3 >nul
start http://localhost:5173
echo Done. You may keep this launcher window open or close it.

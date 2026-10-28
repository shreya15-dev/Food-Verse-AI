# Food Verse AI - PowerShell Concurrent Launcher
Write-Host "========================================================" -ForegroundColor Green
Write-Host "             FOOD VERSE AI - FULL-STACK                " -ForegroundColor Cyan
Write-Host "   'Smarter Food Choices. Safer Kitchens. Healthier Living.'" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Flask Backend in a new PowerShell window
Write-Host "[1/2] Starting Flask Backend on http://127.0.0.1:5000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$baseDir\backend'; Write-Host '--- Food Verse AI Backend ---' -ForegroundColor Green; python app.py"

# Start Vite Frontend in a new PowerShell window
Write-Host "[2/2] Starting React + Vite Frontend on http://localhost:5173..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$baseDir\frontend'; Write-Host '--- Food Verse AI Frontend ---' -ForegroundColor Cyan; npm run dev"

Start-Sleep -Seconds 3
Write-Host ""
Write-Host "Opening web browser at http://localhost:5173..." -ForegroundColor Green
Start-Process "http://localhost:5173"

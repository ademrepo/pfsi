# One-Click Setup for Windows
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Development Environment Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found in PATH." -ForegroundColor Red
    exit 1
}

# 2. Virtual Environment
if (-not (Test-Path "venv")) {
    Write-Host "`nCreating virtual environment (venv)..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "`nvirtual environment already exists." -ForegroundColor Gray
}

# 3. Install Dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Host "Error installing dependencies." -ForegroundColor Red
    exit 1
}

# 4. Initialize Database
Write-Host "`nInitializing database..." -ForegroundColor Yellow
# Run our robust Python initialization script
.\venv\Scripts\python init_db.py

# 5. Start Servers
Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Starting servers..." -ForegroundColor Yellow

# Start Django in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Django Backend (Port 8000)'; .\venv\Scripts\python manage.py runserver"

# Start Frontend in a new window
if (Test-Path "..\frontend") {
    Push-Location "..\frontend"
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
        npm install
    }
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'React Frontend'; npm run dev"
    Pop-Location
} else {
    Write-Host "Frontend directory not found at ..\frontend" -ForegroundColor Red
}

Write-Host "`nYour app should be running shortly." -ForegroundColor Green
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000 (or 3001 if 3000 is busy)"
Write-Host "Login: admin / password123"
Write-Host "`nPress any key to exit this setup window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

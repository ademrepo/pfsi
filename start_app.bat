@echo off
echo 🚀 Starting PF KHRA Transport ^& Logistics Management System...
echo.

REM Check if npm is installed
where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Error: npm is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Install dependencies if needed
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

if not exist "backend\venv" (
    echo 🐍 Setting up Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

echo 🔧 Initializing database...
cd backend
call venv\Scripts\activate
python ../scripts/init_db.py --reset --seed
python manage.py migrate --fake core 0013
python manage.py migrate
cd ..

echo 🌐 Starting servers...
echo.
echo Frontend will be available at: http://localhost:3000
echo Backend API will be available at: http://127.0.0.1:8000
echo Django Admin at: http://127.0.0.1:8000/admin/
echo.
echo Default login: admin / password123
echo.
echo Email: par défaut les emails s'affichent dans la console (console backend).
echo Pour activer un vrai envoi SMTP, définissez EMAIL_HOST / EMAIL_HOST_USER / EMAIL_HOST_PASSWORD avant de lancer.
echo Exemple: voir docs\\email_smtp.md
echo.

REM Start both servers using npm scripts
start "" cmd /k "npm run backend"
timeout /t 3 >nul
start "" cmd /k "npm run dev"

echo ✅ Servers started successfully!
echo.
echo 📝 Note: Two terminal windows will open - one for backend, one for frontend
echo 🚪 The application should open automatically in your browser
echo.
pause

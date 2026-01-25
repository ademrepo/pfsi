# 🚀 PROJET SI Transport & Logistics - Dev Cheat Sheet

## 📋 Table of Contents
- [🔧 Quick Start](#-quick-start)
- [🏗️ Project Structure](#️-project-structure)
- [⚙️ Backend Commands](#️-backend-commands)
- [🌐 Frontend Commands](#-frontend-commands)
- [🧪 Testing](#-testing)
- [🔐 Authentication](#-authentication)
- [📊 Analytics API](#-analytics-api)
- [🔧 Troubleshooting](#-troubleshooting)
- [🚀 Production](#-production)

---

## 🔧 Quick Start

### 🚀 One-Click Setup (Windows)
```bash
# Clone and run
git clone <repository-url>
.\start_app.bat
```

### 📦 NPM Scripts (Recommended)
```bash
# Install all dependencies
npm run setup

# Initialize database with sample data
npm run init-db

# Start both backend and frontend
npm run start
```

### 🛠️ Manual Setup
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python ..\scripts\init_db.py
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 🏗️ Project Structure

```
pfsi/
├── 📁 backend/              # Django Backend
│   ├── 🐍 manage.py         # Django management
│   ├── 📁 core/            # Models, Views, Serializers
│   ├── 📁 mon_projet/      # Settings & URLs
│   └── 📁 scripts/         # Database scripts
├── 📁 frontend/            # React Frontend
│   ├── 📁 src/             # Source code
│   ├── 📄 index.html       # Main HTML
│   └── 📦 package.json     # Dependencies
├── 📁 scripts/             # Test & Utility Scripts
│   ├── 🧪 tests.py         # Backend tests
│   ├── 🔍 test_backend_analytics.py
│   └── 📊 test_backend_simple.py
├── 📄 dev_cheat_sheet.md   # This file
└── 📄 start_app.bat        # Windows startup script
```

---

## ⚙️ Backend Commands

### 🗄️ Database Operations
```bash
# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser

# Reset database (dev only)
rm db.sqlite3
python ..\scripts\init_db.py
python manage.py migrate
```

### 🧪 Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### 🔧 Development
```bash
# Start development server
python manage.py runserver

# Create new migration
python manage.py makemigrations

# Check for issues
python manage.py check
```

---

## 🌐 Frontend Commands

### 📦 Package Management
```bash
# Install dependencies
npm install

# Install specific package
npm install [package-name]

# Update all packages
npm update
```

### 🚀 Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### 🧪 Testing
```bash
# Run tests (if configured)
npm test

# Run tests with coverage
npm run test:coverage
```

---

## 🧪 Testing

### 📁 Test Files Location
- **Backend Tests**: `scripts/tests.py`
- **Analytics Tests**: `scripts/test_backend_analytics.py`
- **Simple Tests**: `scripts/test_backend_simple.py`

### 🏃 Running Tests

#### Backend Tests
```bash
# From project root
python -m unittest scripts.tests -v

# From backend directory
python manage.py test
```

#### Test Scripts
```bash
# Analytics endpoint test
python scripts/test_backend_analytics.py

# Simple authentication test
python scripts/test_backend_simple.py
```

### 📊 Test Coverage
```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run --source='.' manage.py test

# Generate report
coverage report
coverage html  # Creates htmlcov/ directory
```

---

## 🔐 Authentication

### 📡 API Endpoints
```bash
# Login
POST /api/auth/login/
Body: { "username": "admin", "password": "password123" }

# Logout
POST /api/auth/logout/

# Get current user
GET /api/auth/me/

# Get CSRF token
GET /api/auth/csrf/

# Password reset request
POST /api/auth/password-reset/request/
Body: { "email": "user@example.com" }

# Password reset confirm
POST /api/auth/password-reset/confirm/
Body: { "token": "token", "new_password": "newpass", "new_password_confirm": "newpass" }
```

### 🔑 Default Credentials
- **Username**: `admin`
- **Password**: `password123`
- **Email**: `admin@example.com`

---

## 📊 Analytics API

### 📈 Summary Endpoint
```bash
GET /api/analytics/summary/
```

### 🔍 Advanced Analytics
```bash
GET /api/analytics/advanced/?start=YYYY-MM-DD&end=YYYY-MM-DD

# Optional parameters:
# - fuel_price_per_liter (default: 1.5)
# - driver_cost_per_hour (default: 8.0)
# - vehicle_cost_per_km (default: 0.3)
# - cap_shipments_per_vehicle_per_day (default: 30)
# - cap_shipments_per_driver_per_day (default: 25)
# - working_days_per_month (default: 22)
```

### 📊 Response Structure
```json
{
  "shipments": {
    "total": 100,
    "delayed": 5,
    "series": [...]
  },
  "revenue": {...},
  "routes": {...},
  "fuel": {...},
  "incidents": {...},
  "profitability": {...},
  "staffing": {...},
  "map": {...}
}
```

---

## 🔧 Troubleshooting

### 🚨 Common Issues

#### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

#### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Database Issues
```bash
# Soft reset
python ..\scripts\init_db.py
python manage.py migrate

# Hard reset (development only)
rm db.sqlite3
python ..\scripts\init_db.py
python manage.py migrate
```

#### Frontend Build Issues
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### Authentication Problems
```bash
# Clear browser cookies and cache
# Ensure CSRF token is being sent
# Check if session is active
```

### 🐛 Debug Commands
```bash
# Check Django settings
python manage.py check --deploy

# View migration history
python manage.py showmigrations

# Check installed packages
pip list

# Check Node.js version
node --version
npm --version
```

---

## 🚀 Production

### 📦 Build Process
```bash
# Build frontend
cd frontend
npm run build

# Collect static files (if configured)
cd backend
python manage.py collectstatic
```

### ⚙️ Production Settings
```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 🌐 Deployment
- Use WSGI/ASGI server (Gunicorn, uWSGI)
- Configure reverse proxy (Nginx)
- Set up SSL/TLS certificates
- Configure database (PostgreSQL recommended)

---

## 📚 Additional Resources

### 📖 Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)

### 🛠️ Development Tools
- **IDE**: Visual Studio Code
- **Extensions**: Python, ESLint, Prettier, Django
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Version Control**: Git

### 📞 Support
- Check this cheat sheet first
- Review error messages carefully
- Check browser developer tools
- Check Django logs
- Ask team members

---

## 🎯 Quick Reference

| Command | Description |
|---------|-------------|
| `npm run setup` | Install all dependencies |
| `npm run init-db` | Initialize database |
| `npm run start` | Start both servers |
| `python manage.py runserver` | Start Django server |
| `npm run dev` | Start React dev server |
| `python manage.py test` | Run backend tests |
| `npm test` | Run frontend tests |

---

*Last updated: January 2026* 📅
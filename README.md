# 🚀 PF KHRA - Transport & Logistics Management

## Quick Start

### Option 1: One-Click Start (Recommended)
```bash
git clone https://github.com/ademrepo/pfsi.git
cd pfsi
.\start_app.bat
```

### Option 2: Manual Setup
```bash
# 1. Clone and setup
git clone https://github.com/ademrepo/pfsi.git
cd pfsi
npm run install-all

# 2. Start both servers
npm run start
```

### Option 3: Detailed Setup
```bash
# 1. Clone repository
git clone https://github.com/ademrepo/pfsi.git 16avril
cd 16avril

# 2. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Initialize database
python ../scripts/init_db.py
python manage.py migrate

# Start Django server
python manage.py runserver

# 3. Frontend Setup (New terminal)
cd frontend
npm install
npm run dev
```

## 🌐 Application Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000/api/
- **Django Admin**: http://127.0.0.1:8000/admin/

**Default Login**: admin / password123

## 📖 Detailed Documentation
For comprehensive setup instructions, troubleshooting, and development workflow, see:
- [Server Workflow Guide](docs/SERVER_WORKFLOW.md)
- [Testing Workflow](docs/TESTING_WORKFLOW.md)
- [API Documentation](docs/API_ANALYTICS_AND_AUTH.md)

---

## ⚠️ Incidents & Alertes

- **UI**:
  - `Incidents` : http://localhost:3000/incidents
  - `Alertes` : http://localhost:3000/alertes
- **API**:
  - `GET/POST` `/api/incidents/` (pièces jointes via `multipart/form-data`, champ `files`)
  - `GET` `/api/alertes/` + `POST` `/api/alertes/{id}/mark_read/`
- **Uploads (dev)**:
  - Les fichiers (docs/photos) sont servis par Django en mode `DEBUG` via `/media/`.

## 🔧 Development Workflow

### Daily Setup
```bash
# Get latest changes
git pull origin main

# Backend (Terminal 1)
cd backend
venv\Scripts\activate
python manage.py runserver

# Frontend (Terminal 2)
cd frontend
npm run dev
```

### Git Workflow
```bash
# Make changes...
git add .
git commit -m "Clear description of changes"
git push origin main
```

---
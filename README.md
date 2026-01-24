# 🚀 PF KHRA - Transport & Logistics Management

### 1. Clone Repository
```bash
git clone https://github.com/ademrepo/pfsi.git 16avril
cd 16avril
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Initialize database
python ../scripts/init_db.py
python manage.py migrate

# Start Django server
python manage.py runserver
```

### 3. Frontend Setup
```bash
# New terminal
cd frontend
npm install
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000/api/
- **Django Admin**: http://127.0.0.1:8000/admin/

**Login**: admin / password123

---

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

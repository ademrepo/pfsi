# 🚀 PF KHRA - Transport & Logistics Management

Système de gestion de transport et livraison avec Django backend + React frontend + SQLite.

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/ademrepo/pfsi.git
cd pfkhra\si\16avril

# 2. Setup Python environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Initialize database (auto-fixes foreign keys)
python scripts/init_db.py

# 4. Start servers
# Terminal 1 - Backend:
python manage.py runserver

# Terminal 2 - Frontend:
cd frontend
npm install
npm run dev
```

**Access**: http://localhost:3000 | **Login**: admin / password123

---

## 📋 Daily Development Workflow

### Morning Setup
```bash
git pull origin adot
venv\Scripts\activate
python scripts/init_db.py  # if needed
python manage.py runserver  # Terminal 1
cd frontend && npm run dev  # Terminal 2
```

### Development Cycle
```bash
# Make changes...
git status
git add .
git commit -m "Clear description of changes"
git push origin adot
```

### End of Day
```bash
git add .
git commit -m "WIP: daily progress"
git push origin adot
```

---

## 🔧 Essential Git Commands

### Daily Workflow
```bash
git pull origin adot          # Get latest changes
git status                    # Check what's modified
git add .                     # Stage all changes
git commit -m "Clear message" # Commit with good message
git push origin adot          # Push to GitHub
```

### Problem Solving
```bash
git log --oneline -10         # Recent commits
git diff                      # See unstaged changes
git checkout -- file.py       # Undo file changes
git reset --soft HEAD~1       # Undo last commit (keep changes)
```

### Branch Management
```bash
git checkout -b feature/name  # Create feature branch
git checkout adot             # Back to main
git merge feature/name        # Merge feature
git branch -d feature/name    # Delete merged branch
```

---

## 🗄️ Database Management

### Initialize/Reset Database
```bash
python scripts/init_db.py      # Fresh setup (schema + data only)
python scripts/init_db.py --reset  # Complete reset
python manage.py migrate       # Apply Django migrations
```

### Fix Database Issues
```bash
python manage.py migrate           # Apply Django migrations
python simple_test.py              # Test authentication
```

### After SQL Changes
```bash
python scripts/init_db.py --reset
python manage.py migrate
git add db/ && git commit -m "Update DB: description"
```

---

## 🚨 Common Issues & Solutions

### Migration Errors
```bash
# Reset database and reapply migrations
python scripts/init_db.py --reset
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Port Conflicts
```bash
# Kill process on port 8000 (Django)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process on port 3000 (Frontend)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Git Conflicts
```bash
git pull origin adot
# Resolve conflicts in files (look for <<<<<<<)
git add resolved_file.py
git commit -m "Resolve merge conflicts"
git push origin adot
```

---

## 📱 Project Structure

```
16avril/
├── core/                 # Django app (models, views, serializers)
│   ├── models.py         # Django models with business logic
│   ├── signals.py        # Django signals (replaces SQL triggers)
│   └── migrations/       # Django migrations
├── mon_projet/           # Django settings
├── frontend/             # React app
├── scripts/              # Utility scripts
│   └── init_db.py        # Database initialization (schema + data only)
├── db/                   # SQL schema and data (no triggers)
├── requirements.txt       # Python dependencies
└── README.md            # This file
```

**🔧 Architecture Change**: Now using **pure Django** - no SQL triggers! All business logic is handled by Django models and signals.

---

## 🎯 Best Practices

### Git Commits
- ✅ "Add user authentication endpoint"
- ✅ "Fix expedition display bug"
- ✅ "Update requirements.txt with pinned versions"
- ❌ "fix"
- ❌ "update"
- ❌ "changes"

### Before Pushing
- [ ] Tests pass (`python simple_test.py`)
- [ ] No migration errors (`python manage.py migrate --check`)
- [ ] Clear commit message
- [ ] Django models managed=True (no SQL triggers)

### Code Quality
- Small, frequent commits
- Pull before push
- Use feature branches for big changes
- Test before committing

---

## 🔐 Access Information

### Default Login
- **Username**: admin
- **Password**: password123

### Application URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000/api/
- **Django Admin**: http://127.0.0.1:8000/admin/

### Test Users (all password: password123)
- `admin` - Administrator
- `agent1` - Transport Agent
- `comptable1` - Accountant
- `logistique1` - Logistics Manager

---

## 📦 Dependencies

### Backend (requirements.txt)
- Django 4.2.9
- djangorestframework 3.14.0
- django-cors-headers 4.3.1
- python-decouple 3.8
- Pillow 10.1.0

### Frontend (package.json)
- React 18.2.0
- React Router DOM 6.20.0
- Axios 1.6.2
- Vite 5.0.8

---

## 🆘 Emergency Procedures

### Backup Before Big Changes
```bash
git tag backup-$(date +%Y%m%d-%H%M%S)
git push origin --tags
```

### Rollback
```bash
git reflog                    # See previous states
git reset --hard HEAD@{5}     # Go back to stable state
git push --force-with-lease origin adot
```

### Critical Issues
1. Create GitHub issue
2. Tag stable version: `git tag stable-$(date +%Y%m%d)`
3. Work on hotfix branch: `git checkout -b hotfix/issue`

---

**🚀 Ready for development! This setup uses pure Django with no SQL triggers for better reliability and maintainability.**

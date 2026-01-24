# 👥 Collaborator Workflow Guide

## 🚀 Quick Setup for New Collaborators

### 1. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/ademrepo/pfsi.git
cd pfkhra\si\16avril

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies (Python 3.14 compatible)
pip install -r requirements.txt

# Initialize database (pure Django - no SQL triggers)
python scripts/init_db.py
python manage.py migrate
```

### 2. Start Development
```bash
# Terminal 1 - Backend
python manage.py runserver

# Terminal 2 - Frontend (in parent directory)
cd ..\frontend
npm install
npm run dev
```

**Access**: http://localhost:3000 | **Login**: admin / password123

---

## 📋 Daily Workflow

### 🌅 Morning Setup
```bash
# Get latest changes
git pull origin adot

# Activate environment
venv\Scripts\activate

# Start servers
python manage.py runserver        # Terminal 1
cd ..\frontend && npm run dev     # Terminal 2
```

### 💻 Development Cycle
```bash
# Make your changes...
git status                        # Check what's modified
git add .                         # Stage all changes
git commit -m "Clear description" # Commit with good message
git push origin adot              # Push to GitHub
```

### 🌆 End of Day
```bash
git add .
git commit -m "WIP: daily progress"
git push origin adot
```

---

## 🔧 Important Notes

### ✅ **What's Different Now:**
- **Pure Django setup** - no SQL triggers
- **No database issues** - migrations work perfectly
- **Clean codebase** - redundant files removed
- **Python 3.14 compatible** - all dependencies work

### 🚫 **What You DON'T Need:**
- ❌ SQL triggers (removed)
- ❌ Database integrity scripts (not needed)
- ❌ Complex setup procedures
- ❌ Migration fixes

### ✅ **What You DO Need:**
- ✅ Just `python scripts/init_db.py` for fresh setup
- ✅ Standard Django migrations
- ✅ Regular Git workflow

---

## 🎯 Git Best Practices

### ✅ **Good Commit Messages:**
```
✅ "Add user authentication endpoint"
✅ "Fix expedition display bug" 
✅ "Update requirements.txt with pinned versions"
✅ "Implement client code generation via Django signals"
```

### ❌ **Bad Commit Messages:**
```
❌ "fix"
❌ "update"
❌ "changes"
❌ "wip"
```

### 🔄 **Before Pushing:**
- [ ] Tests pass (`python simple_test.py`)
- [ ] No migration errors (`python manage.py migrate --check`)
- [ ] Clear commit message
- [ ] Both servers running

---

## 🚨 Troubleshooting

### Database Issues?
```bash
# Reset database (rarely needed)
python scripts/init_db.py --reset
python manage.py migrate
```

### Port Conflicts?
```bash
# Kill process on port 8000 (Django)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process on port 3000 (Frontend)  
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Module Not Found?
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏗️ Project Structure

```
pfkhra/si/16avril/
├── core/
│   ├── models.py          # Django models + signals
│   ├── views.py           # API endpoints
│   ├── serializers.py     # Data serialization
│   └── migrations/        # Django migrations
├── scripts/
│   └── init_db.py         # Database initialization
├── db/
│   ├── schema.sql         # Table definitions
│   └── data.sql           # Initial data
├── requirements.txt        # Python dependencies
└── README.md              # Complete documentation

../frontend/                # React app (separate folder)
```

---

## 🔐 Access Information

### Default Login
- **Username**: `admin`
- **Password**: `password123`

### Application URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000/api/
- **Django Admin**: http://127.0.0.1:8000/admin/

---

## 🎉 Key Benefits

✅ **Zero database problems** - pure Django setup  
✅ **Easy setup** - just clone and run  
✅ **No SQL triggers** - Django signals instead  
✅ **Clean codebase** - optimized and maintainable  
✅ **Python 3.14 ready** - all dependencies compatible  

---

**🚀 Welcome to the team! The setup is designed to be smooth and problem-free.**

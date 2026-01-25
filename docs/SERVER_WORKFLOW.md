# 🚀 Server Workflow Guide

This guide provides step-by-step instructions for running the PF KHRA Transport & Logistics Management System servers and accessing the application.

## 📋 Prerequisites

Before starting, ensure you have the following installed:
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** (for cloning and version control)

## 🛠️ Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ademrepo/pfsi.git
cd pfsi
```

### 2. Install Dependencies
```bash
# Install backend and frontend dependencies
npm run install-all
```

## 🚀 Quick Start (Recommended)

### Option 1: Using Package.json Scripts (Easiest)
```bash
# Initialize database and start both servers simultaneously
npm run start
```

This command will:
- Start the Django backend server on port 8000
- Start the React frontend development server on port 3000
- Open both applications in your browser

### Option 2: Manual Setup (More Control)

#### Step 1: Backend Setup
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Initialize database
python ../scripts/init_db.py

# Run migrations
python manage.py migrate

# Start Django development server
python manage.py runserver
```

**Backend will be available at:** http://127.0.0.1:8000/

#### Step 2: Frontend Setup
```bash
# Open new terminal window/tab
cd frontend

# Install dependencies (if not already done)
npm install

# Start React development server
npm run dev
```

**Frontend will be available at:** http://localhost:3000/

## 🌐 Application Access Points

### Frontend Application
- **Main Application:** http://localhost:3000/
- **Login Page:** http://localhost:3000/login
- **Dashboard:** http://localhost:3000/dashboard
- **Analytics:** http://localhost:3000/analytics

### Backend API
- **API Base URL:** http://127.0.0.1:8000/api/
- **Django Admin:** http://127.0.0.1:8000/admin/

### Default Credentials
- **Username:** admin
- **Password:** password123

## 📁 Key Application Sections

### Admin Panel (http://localhost:3000/admin)
- User Management
- Audit Logs
- System Configuration

### Agent Panel (http://localhost:3000/agent)
- Client Management
- Expedition Management
- Invoice Management
- Payment Tracking
- Incident Reporting
- Tournee Management

### Analytics Dashboard (http://localhost:3000/analytics)
- Business Analytics
- Route Analysis
- Revenue Tracking
- Fuel Consumption Reports

## 🔧 Development Workflow

### Daily Development Routine
```bash
# 1. Pull latest changes
git pull origin main

# 2. Start backend server (Terminal 1)
cd backend
venv\Scripts\activate
python manage.py runserver

# 3. Start frontend server (Terminal 2)
cd frontend
npm run dev

# 4. Access application at http://localhost:3000
```

### Database Operations
```bash
# Initialize fresh database
npm run init-db

# Run migrations after model changes
cd backend
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### Testing
```bash
# Run backend tests
cd backend
python manage.py test

# Run specific test file
python manage.py test test_analytics
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # macOS/Linux

# Kill process using port 8000
taskkill /PID <process_id> /F  # Windows
kill -9 <process_id>  # macOS/Linux
```

#### 2. Virtual Environment Issues
```bash
# Recreate virtual environment
cd backend
rm -rf venv  # or delete venv folder manually
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Database Issues
```bash
# Reset database (WARNING: This will delete all data)
cd backend
rm db.sqlite3
python ../scripts/init_db.py
python manage.py migrate
```

#### 4. Frontend Build Issues
```bash
# Clear npm cache and reinstall
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Environment Variables

If you need to configure environment variables, create a `.env` file in the backend directory:

```bash
# backend/.env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

## 🚢 Production Deployment

### Build Frontend for Production
```bash
cd frontend
npm run build
```

### Collect Static Files (Backend)
```bash
cd backend
python manage.py collectstatic
```

### Run Production Server
```bash
cd backend
python manage.py runserver --insecure
```

## 📞 Support

If you encounter issues:
1. Check the console/terminal for error messages
2. Verify all dependencies are installed
3. Ensure ports 8000 and 3000 are available
4. Check the troubleshooting section above
5. Review the project documentation in the `docs/` folder

## 🔄 Git Workflow

### Making Changes
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes...

# Add and commit changes
git add .
git commit -m "Clear description of changes"

# Push to remote
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Updating from Main
```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Switch back to your feature branch
git checkout feature/your-feature-name

# Rebase your changes on top of latest main
git rebase main
```

---

**Note:** This workflow assumes you're working on a Windows system. For macOS/Linux, adjust the virtual environment activation commands accordingly.
# 🚀 Quick Start Guide - Fix Login Issue

## The Problem
You're getting "Échec de la connexion" when trying to login with `admin/password123`.

## ✅ Good News!
I ran diagnostic tests and **the backend authentication works perfectly**! The issue is that you need to have **both servers running**.

## 🔧 Solution: Start Both Servers

### Step 1: Apply Django Migrations (One-time setup)

```bash
cd "c:\L3 ISIL A 2025-2026\PFKHRA\pfkhra si\16avril"

# Activate virtual environment
venv\Scripts\activate

# Apply migrations (creates django_session table)
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  No migrations to apply.
```

### Step 2: Start Django Backend (Terminal 1)

```bash
cd "c:\L3 ISIL A 2025-2026\PFKHRA\pfkhra si\16avril"

# Activate virtual environment
venv\Scripts\activate

# Start Django server
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
```

✅ **Leave this terminal running!**

### Step 2: Start Frontend (Terminal 2 - NEW TERMINAL)

```bash
cd "c:\L3 ISIL A 2025-2026\PFKHRA\pfkhra si\frontend"

# Start Vite dev server
npm run dev
```

**Expected output:**
```
VITE ready in XXX ms
Local: http://localhost:3000/
```

✅ **Leave this terminal running too!**

### Step 3: Login

1. Open browser: http://localhost:3000
2. Enter credentials:
   - Username: `admin`
   - Password: `password123`
3. Click "Se connecter"

## 🐛 Debugging

I've added debug logging to help identify issues. When you try to login, you'll see detailed logs in the **Django terminal** showing:
- ✓ Incoming login requests
- ✓ Authentication success/failure
- ✓ Session creation
- ✓ Any errors

### If Login Still Fails

Check the Django terminal for debug output like:
```
============================================================
[LOGIN] Incoming login request
  Username: admin
  Password provided: Yes
  Client IP: 127.0.0.1
============================================================

[LOGIN] ✓ Authentication successful for user: admin
  User ID: 1
  Role: ADMIN
  Creating session...
  Session created: xyz123...
[LOGIN] ✓ Returning success response
```

## 📝 Test Credentials

All test users have password: `password123`

- `admin` - Administrateur
- `agent1` - Agent de transport
- `comptable1` - Comptable
- `logistique1` - Responsable logistique

## ⚠️ Common Issues

### "Connection refused" or "Network error"
- Make sure Django server is running on port 8000
- Check: http://127.0.0.1:8000/api/auth/csrf/ (should return JSON)

### "CSRF token missing"
- The frontend automatically handles this
- Make sure you're accessing via http://localhost:3000 (not 127.0.0.1:3000)

### Port already in use
```bash
# Django (port 8000)
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (port 3000)
# Find and kill process using port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

## 🧪 Verify Backend Works

Run this test script to verify the backend:
```bash
cd "c:\L3 ISIL A 2025-2026\PFKHRA\pfkhra si\16avril"
python test_login_api.py
```

Should show: `✓ All tests passed!`

---

**Need more help?** Check the Django terminal logs when you try to login - they'll show exactly what's happening!

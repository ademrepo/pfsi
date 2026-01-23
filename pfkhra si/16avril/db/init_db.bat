@echo off
REM ============================================
REM Database Initialization Script
REM This script creates a fresh database from SQL files
REM ============================================

echo ============================================
echo Database Initialization
echo ============================================
echo.

REM Check if database already exists
if exist "..\db.sqlite3" (
    echo WARNING: Database file already exists!
    echo.
    set /p confirm="Do you want to DELETE the existing database and create a new one? (yes/no): "
    if /i not "%confirm%"=="yes" (
        echo.
        echo Operation cancelled.
        pause
        exit /b 1
    )
    echo.
    echo Deleting existing database...
    del "..\db.sqlite3"
)

echo Creating new database...
echo.

REM Create database and run SQL files in order
echo [1/3] Creating schema...
sqlite3 ..\db.sqlite3 < schema.sql
if errorlevel 1 (
    echo ERROR: Failed to create schema
    pause
    exit /b 1
)

echo [2/3] Creating triggers...
sqlite3 ..\db.sqlite3 < triggers.sql
if errorlevel 1 (
    echo ERROR: Failed to create triggers
    pause
    exit /b 1
)

echo [3/3] Inserting data...
sqlite3 ..\db.sqlite3 < data.sql
if errorlevel 1 (
    echo ERROR: Failed to insert data
    pause
    exit /b 1
)

echo.
echo ============================================
echo Database created successfully!
echo Location: ..\db.sqlite3
echo ============================================
echo.
echo You can now use the database in your application.
echo.
pause

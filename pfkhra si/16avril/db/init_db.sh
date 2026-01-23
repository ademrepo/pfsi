#!/bin/bash
# ============================================
# Database Initialization Script (Linux/Mac)
# This script creates a fresh database from SQL files
# ============================================

echo "============================================"
echo "Database Initialization"
echo "============================================"
echo ""

# Check if database already exists
if [ -f "../db.sqlite3" ]; then
    echo "WARNING: Database file already exists!"
    echo ""
    read -p "Do you want to DELETE the existing database and create a new one? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo ""
        echo "Operation cancelled."
        exit 1
    fi
    echo ""
    echo "Deleting existing database..."
    rm "../db.sqlite3"
fi

echo "Creating new database..."
echo ""

# Create database and run SQL files in order
echo "[1/3] Creating schema..."
sqlite3 ../db.sqlite3 < schema.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create schema"
    exit 1
fi

echo "[2/3] Creating triggers..."
sqlite3 ../db.sqlite3 < triggers.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create triggers"
    exit 1
fi

echo "[3/3] Inserting data..."
sqlite3 ../db.sqlite3 < data.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to insert data"
    exit 1
fi

echo ""
echo "============================================"
echo "Database created successfully!"
echo "Location: ../db.sqlite3"
echo "============================================"
echo ""
echo "You can now use the database in your application."
echo ""

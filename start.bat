@echo off
title POS - Forn Al Asli

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed.
    echo Download from: https://python.org/downloads
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

echo Starting POS server...
echo Browser will open automatically.
echo Press Ctrl+C to stop.
echo.

python server.py

pause

@echo off
title ZARVIS // Autonomous Desktop AI
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   🤖 ZARVIS / ULTRON AI — AUTONOMOUS WORKSTATION SYSTEM
echo ============================================================
echo.

:: 1. Check Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH!
    echo [!] Please install Python 3.11 or 3.12 from python.org
    pause
    exit /b 1
)

:: 2. Check Virtual Environment
if not exist "venv\Scripts\python.exe" (
    echo [*] Creating virtual environment (venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] Failed to create venv!
        pause
        exit /b 1
    )
    echo [*] Installing dependencies from requirements.txt...
    venv\Scripts\pip.exe install -r requirements.txt
)

:: 3. Check Configuration
if not exist "config\api_keys.json" (
    if exist "config\api_keys.json.example" (
        echo [*] Initializing config\api_keys.json from template...
        copy "config\api_keys.json.example" "config\api_keys.json" >nul
    )
)

:: 4. Launch ZARVIS
echo [*] Launching ZARVIS AI Workstation Interface...
echo.
venv\Scripts\python.exe main.py

if %errorlevel% neq 0 (
    echo.
    echo [!] ZARVIS exited with code %errorlevel%.
    pause
)

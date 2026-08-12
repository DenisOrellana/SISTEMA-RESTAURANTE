@echo off
title Sistema de Restaurante
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe ejecutar.py
) else (
    python ejecutar.py
)
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se encontro Python. Instala Python desde https://python.org
    pause
)

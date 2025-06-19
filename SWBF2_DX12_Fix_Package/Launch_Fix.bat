@echo off
title SWBF2 DX12 Fix Launcher

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ========================================================
echo   STAR WARS BATTLEFRONT II - DX12 FIX LAUNCHER
echo ========================================================
echo.

REM Check if we're in the right directory
if not exist "SWBF2_DX12_Complete_Fix.py" (
    echo ERROR: Fix script not found!
    echo Make sure this file is in the SWBF2_DX12_Fix_Package directory.
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.6+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo Found Python installation.
echo.

REM Ask user what they want to do
echo What would you like to do?
echo.
echo 1. Run System Verification (recommended first-time)
echo 2. Apply DX12 Fix (main fix)
echo 3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Running system verification...
    echo.
    python verify_system.py
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo ========================================================
    echo                    IMPORTANT NOTICE
    echo ========================================================
    echo.
    echo This fix will modify your game settings and registry.
    echo All changes are reversible with the restore script.
    echo.
    echo For best results, run this as Administrator:
    echo 1. Right-click this file
    echo 2. Select "Run as administrator"
    echo.
    set /p confirm="Continue anyway? (Y/N): "
    if /i not "%confirm%"=="Y" (
        echo.
        echo Fix cancelled by user.
        goto :end
    )
    
    echo.
    echo Applying SWBF2 DX12 fixes...
    echo.
    python SWBF2_DX12_Complete_Fix.py
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo Exiting...
    goto :end
)

echo.
echo Invalid choice. Please run the script again.

:end
echo.
pause 
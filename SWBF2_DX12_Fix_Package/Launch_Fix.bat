@echo off
setlocal enabledelayedexpansion
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

REM Check for administrator privileges
net session >nul 2>&1
if %errorlevel% == 0 (
    set "isAdmin=true"
    echo Running with Administrator privileges.
) else (
    set "isAdmin=false"
    echo Running with standard user privileges.
)
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    if "%isAdmin%"=="true" (
        echo Would you like to automatically install Python?
        echo This will download and install Python 3.11 from the official website.
        echo.
        set /p installPython="Install Python automatically? (Y/N): "
        if /i "!installPython!"=="Y" (
            echo.
            echo Downloading and installing Python...
            echo This may take a few minutes...
            echo.
            powershell -Command "& { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile '%temp%\python-installer.exe' }"
            if exist "%temp%\python-installer.exe" (
                echo Installing Python...
                "%temp%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
                echo.
                echo Python installation completed. Refreshing environment...
                echo Please restart this script to use the new Python installation.
                del "%temp%\python-installer.exe" >nul 2>&1
                pause
                exit /b 0
            ) else (
                echo Failed to download Python installer.
                echo Please install Python manually from https://python.org
                pause
                exit /b 1
            )
        )
    ) else (
        echo To automatically install Python, please run this script as Administrator.
        echo Or install Python manually from https://python.org
    )
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
echo 2. Apply Complete DX12 Fix
echo 3. Apply UI-Only Fix (keeps 3D scaling)
echo 4. Open GUI Version (with manual path selection)
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

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
    echo                    COMPLETE DX12 FIX
    echo ========================================================
    echo.
    echo This fix will modify your game settings and registry.
    echo All changes are reversible with the restore script.
    echo.
    if "%isAdmin%"=="false" (
        echo NOTICE: For best results, run this as Administrator:
        echo 1. Right-click this file
        echo 2. Select "Run as administrator"
        echo.
        set /p confirm="Continue with standard privileges? (Y/N): "
        if /i not "!confirm!"=="Y" (
            echo.
            echo Fix cancelled by user.
            goto :end
        )
    ) else (
        echo Running with Administrator privileges - optimal setup!
        echo.
        set /p confirm="Apply complete DX12 fix? (Y/N): "
        if /i not "!confirm!"=="Y" (
            echo.
            echo Fix cancelled by user.
            goto :end
        )
    )
    
    echo.
    echo Applying SWBF2 Complete DX12 fixes...
    echo.
    python SWBF2_DX12_Complete_Fix.py
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo ========================================================
    echo                     UI-ONLY FIX
    echo ========================================================
    echo.
    echo This fix targets UI artifacts while keeping 3D scaling.
    echo Your resolution scaling benefits will be preserved.
    echo.
    set /p confirm="Apply UI-only fix? (Y/N): "
    if /i not "!confirm!"=="Y" (
        echo.
        echo Fix cancelled by user.
        goto :end
    )
    
    echo.
    echo Applying UI artifact fixes...
    echo.
    python Fix_UI_Artifacts.py
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo ========================================================
    echo                      GUI VERSION
    echo ========================================================
    echo.
    echo Opening GUI version with manual path selection...
    echo This version allows you to specify custom directories.
    echo.
    python SWBF2_GUI_Fix.py
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo Exiting...
    goto :end
)

echo.
echo Invalid choice. Please run the script again.

:end
echo.
pause 
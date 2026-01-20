@echo off
echo ============================================================
echo  BLIND NAVIGATION SYSTEM - WINDOWS STARTUP
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo.
    echo Installing requirements...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo.
)

REM Start the application
echo.
echo Starting application...
echo.
python start.py

pause

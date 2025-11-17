@echo off
REM Qase Reporter - Web UI Launcher
REM This script activates the virtual environment and starts the Streamlit app

echo ========================================
echo   Qase Test Run Reporter - Web UI
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run the following commands first:
    echo   1. python -m venv venv
    echo   2. venv\Scripts\activate.bat
    echo   3. pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found!
    echo.
    echo Please create a .env file with:
    echo   QASE_API_TOKEN=your_token_here
    echo   QASE_PROJECT_CODE=your_project_code
    echo.
    echo The app will start but may not work without configuration.
    echo.
    timeout /t 3
)

REM Start Streamlit app
echo [INFO] Starting Streamlit application...
echo.
streamlit run app.py

REM Deactivate virtual environment on exit
deactivate

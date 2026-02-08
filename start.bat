@echo off
REM Trade Analyzer - Windows Startup Script

echo.
echo ========================================
echo   Trade Analyzer - Startup
echo ========================================
echo.

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create venv
        exit /b 1
    )
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys:
    echo - GEMINI_API_KEY (from https://makersuite.google.com/app/apikey)
    echo - NEWSAPI_KEY (from https://newsapi.org)
    echo - ALPHAVANTAGE_KEY (from https://www.alphavantage.co/api/)
    echo.
)

REM Start server
echo.
echo ========================================
echo Starting Trade Analyzer Server...
echo Server will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python backend/main.py

pause

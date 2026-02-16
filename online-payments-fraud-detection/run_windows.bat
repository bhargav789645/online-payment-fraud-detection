@echo off
REM Run Fraud Detection System - Windows Batch Script

echo.
echo ============================================
echo   Online Payments Fraud Detection System
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Run training script
echo.
echo ============================================
echo   Training ML Models (This may take a few minutes)
echo ============================================
echo.
python training_script.py

REM Check if training was successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo   Training Complete! Starting Flask App...
    echo ============================================
    echo.
    echo Opening http://127.0.0.1:5000 in your browser...
    echo Press Ctrl+C to stop the server
    echo.
    cd app
    python main.py
) else (
    echo.
    echo ERROR: Training failed. Please check the error messages above.
    echo.
    pause
    exit /b 1
)

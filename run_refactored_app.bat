@echo off
echo Starting refactored AgentVerse application...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in the PATH.
    echo Please install Python 3.8 or newer and try again.
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed or not in the PATH.
    echo Please ensure pip is properly installed with Python.
    pause
    exit /b 1
)

:: Check if required packages are installed
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error installing required packages.
        pause
        exit /b 1
    )
)

:: Set the PYTHONPATH environment variable to include the current directory
set PYTHONPATH=%CD%;%PYTHONPATH%

:: Run the application
echo Starting Streamlit interface...
streamlit run src_py/main.py

echo.
echo Press any key to exit...
pause > nul 
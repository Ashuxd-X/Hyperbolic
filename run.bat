@echo off
setlocal enabledelayedexpansion
title Hyperbolic Bot
color 0A

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    echo You can download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if key.txt exists and create it if it doesn't
if not exist key.txt (
    echo Creating key.txt...
    echo Please enter your Hyperbolic API key:
    set /p "API_KEY="
    (
        echo !API_KEY!
    ) > key.txt
    echo API key saved to key.txt
    echo.
)

:: Check if key.txt is empty
findstr /n . key.txt >nul
if errorlevel 1 (
    echo Error: key.txt is empty!
    echo Please enter your Hyperbolic API key:
    set /p "API_KEY="
    (
        echo !API_KEY!
    ) > key.txt
    echo API key saved to key.txt
    echo.
)

:: Check if requirements are installed
echo Checking requirements...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements!
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
)

:: Check if hyper.py exists
if not exist hyper.py (
    echo Error: hyper.py not found!
    echo Please make sure you're running this from the correct folder.
    pause
    exit /b 1
)

:: Run the bot
echo.
echo Starting Hyperbolic Bot...
echo Press Ctrl+C to stop the bot
echo.
python hyper.py

:: If the bot crashes, show error message
if errorlevel 1 (
    echo.
    echo An error occurred while running the bot.
    echo Please check the error message above.
    pause
) 
@echo off
REM Installation script for Windows

echo ================================================
echo Telegram Auto Order Bot - Installation Script
echo ================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python is installed
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Setup configuration
if not exist .env (
    echo Setting up configuration...
    copy .env.example .env
    echo.
    echo ================================================
    echo IMPORTANT: Please edit .env file with your credentials
    echo ================================================
    echo.
    echo You need to set:
    echo   - API_ID from my.telegram.org
    echo   - API_HASH from my.telegram.org
    echo   - BOT_TOKEN from @BotFather
    echo   - ADMIN_IDS your Telegram user ID
    echo.
    echo Edit .env file with notepad or any text editor
    echo.
) else (
    echo Configuration file already exists
)

REM Create logs directory
if not exist logs mkdir logs

echo.
echo ================================================
echo Installation complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Activate virtual environment: venv\Scripts\activate.bat
echo 3. Setup sample data optional: python setup_sample_data.py
echo 4. Run bot: python main.py
echo.
pause

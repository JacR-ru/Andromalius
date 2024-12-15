@echo off
echo Checking for required dependencies...

if not exist ".venv" (
    echo Virtual environment not found. Creating .venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment. Exiting.
        pause
        exit /b
    )
    echo Virtual environment created successfully.
)

call .venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment. Exiting.
    pause
    exit /b
)

echo Virtual environment activated.

if exist requirements.txt (
    echo requirements.txt found. Checking installed dependencies...

    :: Проверяем, установлен ли pip
    python -m pip --version >nul 2>nul
    if %errorlevel% neq 0 (
        echo Pip is not installed. Installing pip...
        python -m ensurepip --upgrade
        python -m pip install --upgrade pip
    )

    python -m pip freeze > installed_packages.txt

    set needs_installation=false

    for /f "tokens=*" %%a in (requirements.txt) do (
        findstr /i "%%a" installed_packages.txt >nul
        if %errorlevel% neq 0 (
            echo Dependency "%%a" not found. Marking for installation.
            set needs_installation=true
        )
    )

    if "%needs_installation%"=="true" (
        echo Installing missing dependencies...
        python -m pip install -r requirements.txt
    ) else (
        echo All dependencies are already installed. Skipping installation.
    )
) else (
    echo requirements.txt not found. Please make sure it exists in the script directory.
    pause
    exit /b
)

echo Running Andromalius script...
python main.py
pause

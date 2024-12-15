#!/bin/bash

echo "Checking for required dependencies..."


if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating .venv..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Exiting."
        exit 1
    fi
    echo "Virtual environment created successfully."
fi


source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Exiting."
    exit 1
fi

echo "Virtual environment activated."


if [ -f "requirements.txt" ]; then
    echo "requirements.txt found. Checking installed dependencies..."

    python3 -m pip --version >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Pip is not installed. Installing pip..."
        python3 -m ensurepip --upgrade
        python3 -m pip install --upgrade pip
    fi

    python3 -m pip freeze > installed_packages.txt

    needs_installation=false

    while IFS= read -r dependency; do
        grep -i "$dependency" installed_packages.txt >/dev/null
        if [ $? -ne 0 ]; then
            echo "Dependency \"$dependency\" not found. Marking for installation."
            needs_installation=true
        fi
    done < requirements.txt

    if [ "$needs_installation" = true ]; then
        echo "Installing missing dependencies..."
        python3 -m pip install -r requirements.txt
    else
        echo "All dependencies are already installed. Skipping installation."
    fi
else
    echo "requirements.txt not found. Please make sure it exists in the script directory."
    exit 1
fi

echo "Running Andromalius script..."
python3 main.py

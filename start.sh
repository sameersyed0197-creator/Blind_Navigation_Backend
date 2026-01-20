#!/bin/bash

echo "============================================================"
echo " BLIND NAVIGATION SYSTEM - MAC/LINUX STARTUP"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Installing requirements..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo ""
fi

# Start the application
echo ""
echo "Starting application..."
echo ""
python start.py

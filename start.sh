#!/bin/bash
# Trade Analyzer - Linux/Mac Startup Script

echo ""
echo "========================================"
echo "  Trade Analyzer - Startup"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create venv"
        exit 1
    fi
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys:"
    echo "- GEMINI_API_KEY (from https://makersuite.google.com/app/apikey)"
    echo "- NEWSAPI_KEY (from https://newsapi.org)"
    echo "- ALPHAVANTAGE_KEY (from https://www.alphavantage.co/api/)"
    echo ""
fi

# Start server
echo ""
echo "========================================"
echo "Starting Trade Analyzer Server..."
echo "Server will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

python backend/main.py

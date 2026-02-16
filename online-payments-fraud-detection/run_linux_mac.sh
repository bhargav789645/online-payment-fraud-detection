#!/bin/bash
# Run Fraud Detection System - Linux/Mac Shell Script

echo ""
echo "============================================"
echo "  Online Payments Fraud Detection System"
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run training script
echo ""
echo "============================================"
echo "   Training ML Models (This may take a few minutes)"
echo "============================================"
echo ""
python3 training_script.py

# Check if training was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "   Training Complete! Starting Flask App..."
    echo "============================================"
    echo ""
    echo "Opening http://127.0.0.1:5000 in your browser..."
    echo "Press Ctrl+C to stop the server"
    echo ""
    cd app
    python3 main.py
else
    echo ""
    echo "ERROR: Training failed. Please check the error messages above."
    echo ""
    exit 1
fi

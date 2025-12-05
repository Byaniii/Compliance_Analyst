#!/bin/bash
# Run the compliance review web application

cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Creating it..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q flask flask-cors pytest
fi

# Run Flask app
echo "🚀 Starting AML/KYC Compliance Review System..."
echo "📱 Open http://localhost:5000 in your browser"
echo "⚠️  Press Ctrl+C to stop"
python app.py

#!/bin/bash

# Resume Evaluator Backend Startup Script

echo "🚀 Starting Resume Evaluator Backend..."

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API documentation available at http://localhost:8000/docs"
echo ""

python main.py 
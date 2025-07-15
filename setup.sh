#!/bin/bash

# Resume Evaluator Complete Setup Script

echo "🚀 Setting up Resume Evaluator Application..."
echo "=============================================="
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed!"
echo ""

# Backend Setup
echo "🐍 Setting up Python Backend..."
echo "-------------------------------"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Frontend Setup
echo "⚡ Setting up Angular Frontend..."
echo "--------------------------------"

cd ../frontend

# Install Node.js dependencies
echo "📥 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo ""

# Create environment file
echo "⚙️ Setting up environment configuration..."
cd ../backend
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ Environment file created. Edit .env if needed."
else
    echo "✅ Environment file already exists."
fi

echo ""
echo "🎉 Setup complete!"
echo "=================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend server:"
echo "   ./start-backend.sh"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   ./start-frontend.sh"
echo ""
echo "3. Open your browser to:"
echo "   Frontend: http://localhost:4200"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Happy coding! 🚀" 
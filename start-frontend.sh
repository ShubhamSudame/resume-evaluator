#!/bin/bash

# Resume Evaluator Frontend Startup Script

echo "🎨 Starting Resume Evaluator Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📥 Installing Node.js dependencies..."
    npm install
fi

# Check if Angular CLI is installed
if ! npx ng version >/dev/null 2>&1; then
    echo "📦 Installing Angular CLI..."
    npm install -g @angular/cli
fi

# Start the development server
echo "🌐 Starting Angular development server on http://localhost:4200"
echo "🔄 Hot reload enabled - changes will automatically refresh the browser"
echo ""

npm start 
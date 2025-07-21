#!/bin/bash

# Resume Evaluator Production Deployment Script
# This script helps deploy the application using Docker Compose

set -e

echo "🚀 Resume Evaluator Production Deployment"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.production .env
    echo "📝 Please edit .env file with your configuration before continuing."
    echo "   Important: Set your GEMINI_API_KEY and secure passwords!"
    exit 1
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo "🔧 Building and starting services..."
echo "   This may take a few minutes on first run..."

# Build and start services
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are healthy
echo "🏥 Checking service health..."

# Wait for MongoDB to be ready
echo "   Waiting for MongoDB..."
until docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
    sleep 2
done
echo "   ✅ MongoDB is ready"

# Wait for application to be ready
echo "   Waiting for Resume Evaluator application..."
until curl -f http://localhost:8000/api/health > /dev/null 2>&1; do
    sleep 2
done
echo "   ✅ Resume Evaluator application is ready"

echo ""
echo "🎉 Deployment completed successfully!"
echo "====================================="
echo "📱 Application URL: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/api/health"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Update application: docker-compose up --build -d"
echo ""
echo "🔐 Don't forget to:"
echo "   - Set your GEMINI_API_KEY in the .env file"
echo "   - Change default passwords in the .env file"
echo "   - Configure your domain in ALLOWED_ORIGINS if deploying to production" 
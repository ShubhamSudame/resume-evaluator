# Docker Deployment Guide for Resume Evaluator

This guide will help you deploy the Resume Evaluator application using Docker and Docker Compose.

## 🏗️ Architecture Overview

The application consists of:
- **Frontend**: Angular 17 application (built and served by FastAPI)
- **Backend**: FastAPI Python application
- **Database**: MongoDB 7.0
- **AI Integration**: Google Gemini 2.5 Flash

## 📋 Prerequisites

1. **Docker** (version 20.10 or higher)
2. **Docker Compose** (version 2.0 or higher)
3. **Google Gemini API Key** (for AI-powered resume evaluation)

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd resume-evaluator
```

### 2. Set Up Environment
```bash
# If you have an existing .env file in the backend directory, copy it to the root
cp backend/.env .env

# Or copy the environment template
cp env.production .env

# Edit the .env file with your configuration
nano .env
```

### 3. Configure Environment Variables

Edit the `.env` file with your settings:

```env
# Required: Your Gemini API Key
GEMINI_API_KEY=your-actual-gemini-api-key-here

# MongoDB Configuration (change these in production)
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=your-secure-password-here
DATABASE_NAME=resume_evaluator

# Security (change in production)
SECRET_KEY=your-super-secret-key-change-this-in-production

# Application Configuration
API_PORT=8000
DEBUG=False
ENVIRONMENT=production

# CORS (add your domain for production)
ALLOWED_ORIGINS=http://localhost:8000,http://your-domain.com
```

### 4. Deploy with Script
```bash
# Make script executable (if not already)
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### 5. Manual Deployment (Alternative)
```bash
# Build and start services
docker-compose up --build -d

# Check logs
docker-compose logs -f
```

## 🌐 Access the Application

Once deployed, access the application at:
- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📁 File Structure

```
resume-evaluator/
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Service orchestration
├── .dockerignore             # Docker build exclusions
├── deploy.sh                 # Deployment script
├── env.production            # Environment template
├── .env                      # Your environment file (create this)
├── frontend/                 # Angular application
├── backend/                  # FastAPI application
│   ├── init-mongo.js        # MongoDB initialization
│   └── requirements.txt     # Python dependencies
└── uploads/                  # Resume uploads (created automatically)
```

## 🔧 Docker Configuration Details

### Multi-Stage Dockerfile
- **Stage 1**: Build Angular frontend with `node:22-alpine`
- **Stage 2**: Serve with Python backend using `python:3.11-slim`
- **Security**: Runs as non-root user
- **Health Check**: Built-in health monitoring

### Docker Compose Services
- **resume-evaluator**: Main application
- **mongodb**: Database with persistent storage
- **Network**: Isolated bridge network
- **Volumes**: Persistent data storage

## 🛠️ Management Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f resume-evaluator
docker-compose logs -f mongodb
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Update Application
```bash
docker-compose up --build -d
```

### Access Database
```bash
# Connect to MongoDB
docker-compose exec mongodb mongosh

# Backup database
docker-compose exec mongodb mongodump --out /backup
```

### Clean Up
```bash
# Stop and remove containers, networks
docker-compose down

# Also remove volumes (⚠️ deletes data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 🔒 Security Considerations

### Production Deployment
1. **Change Default Passwords**: Update MongoDB credentials
2. **Secure Secret Key**: Generate a strong SECRET_KEY
3. **Configure CORS**: Set ALLOWED_ORIGINS to your domain
4. **Use HTTPS**: Configure reverse proxy (nginx/traefik)
5. **Environment Variables**: Never commit .env files

### Example Production .env
```env
GEMINI_API_KEY=your-gemini-api-key
MONGO_ROOT_USERNAME=resume_admin
MONGO_ROOT_PASSWORD=super-secure-password-123
SECRET_KEY=your-256-bit-secret-key-here
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
DEBUG=False
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using port 8000
lsof -i :8000

# Change port in .env
API_PORT=8001
```

**2. MongoDB Connection Issues**
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

**3. Frontend Not Loading**
```bash
# Check if dist folder was built
docker-compose exec resume-evaluator ls -la frontend/dist

# Rebuild frontend
docker-compose build --no-cache resume-evaluator
```

**4. Permission Issues**
```bash
# Fix uploads directory permissions
sudo chown -R $USER:$USER uploads/
chmod 755 uploads/
```

### Health Checks
```bash
# Check application health
curl http://localhost:8000/api/health

# Check MongoDB health
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

## 📊 Monitoring

### Resource Usage
```bash
# View container resource usage
docker stats

# View disk usage
docker system df
```

### Logs Analysis
```bash
# Search for errors
docker-compose logs | grep -i error

# Search for specific patterns
docker-compose logs | grep "resume"
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up --build -d
```

### Database Backup
```bash
# Create backup
docker-compose exec mongodb mongodump --out /backup/$(date +%Y%m%d)

# Copy backup from container
docker cp resume-evaluator-mongodb:/backup ./backup
```

### Database Restore
```bash
# Copy backup to container
docker cp ./backup resume-evaluator-mongodb:/backup

# Restore database
docker-compose exec mongodb mongorestore /backup
```

## 🎯 Next Steps

1. **Set up monitoring** (Prometheus, Grafana)
2. **Configure logging** (ELK stack, Fluentd)
3. **Set up CI/CD** (GitHub Actions, GitLab CI)
4. **Add SSL/TLS** (Let's Encrypt, Certbot)
5. **Configure backups** (Automated database backups)
6. **Set up alerts** (Health check notifications)

## 📞 Support

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify environment variables in `.env`
3. Ensure all prerequisites are met
4. Check the troubleshooting section above

For additional help, refer to the main README.md file. 
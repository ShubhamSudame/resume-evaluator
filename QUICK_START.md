# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Run the Setup Script
```bash
./setup.sh
```

This will:
- ✅ Check prerequisites (Python 3.8+, Node.js 16+)
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all Node.js dependencies
- ✅ Create environment configuration

### 2. Start the Backend Server
```bash
./start-backend.sh
```

The FastAPI server will start on `http://localhost:8000`

### 3. Start the Frontend (in a new terminal)
```bash
./start-frontend.sh
```

The Angular app will start on `http://localhost:4200`

## 🌐 Access Points

- **Frontend Application**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 What You Get

- **Modern UI**: Beautiful drag-and-drop file upload interface
- **File Support**: Upload PDF, DOC, DOCX resumes
- **Real-time Progress**: Live upload tracking
- **API Integration**: FastAPI backend with CORS support
- **Development Ready**: Hot reload for both frontend and backend

## 🔧 Development

- **Frontend**: Angular 17 with TypeScript
- **Backend**: FastAPI with Python
- **Architecture**: Separated frontend/backend with API communication

## 📁 Project Structure

```
resume-evaluator/
├── backend/          # FastAPI Python backend
├── frontend/         # Angular TypeScript frontend
├── setup.sh         # Complete setup script
├── start-backend.sh # Backend startup script
├── start-frontend.sh # Frontend startup script
└── README.md        # Detailed documentation
```

## 🆘 Troubleshooting

If you encounter issues:

1. **Check prerequisites**: Ensure Python 3.8+ and Node.js 16+ are installed
2. **Re-run setup**: `./setup.sh`
3. **Check ports**: Ensure ports 8000 and 4200 are available
4. **Check logs**: Look at terminal output for error messages

## 🎉 You're Ready!

Your Resume Evaluator application is now set up and ready for development! 